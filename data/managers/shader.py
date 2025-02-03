from pathlib import Path
from array import array
import moderngl
from data.constants import ShaderType
from data.shaders.classes import shader_pass_lookup
from data.shaders.protocol import SMProtocol

shader_path = (Path(__file__).parent / '../shaders/').resolve()

SHADER_PRIORITY = [
    ShaderType.CRT,
    ShaderType.CHROMATIC_ABBREVIATION,
    ShaderType.SHAKE,
    ShaderType.BLOOM,
    ShaderType.RAYS,
    ShaderType.GRAYSCALE,
    ShaderType.BASE,
]

pygame_quad_array = array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
])  

opengl_quad_array = array('f', [
    -1.0, -1.0, 0.0, 0.0,
    1.0, -1.0, 1.0, 0.0,
    -1.0, 1.0, 0.0, 1.0,
    1.0, 1.0, 1.0, 1.0,
])

class ShaderManager(SMProtocol):
    def __init__(self, ctx: moderngl.Context, screen_size):
        self._ctx = ctx
        self._ctx.gc_mode = 'auto'

        self._screen_size = screen_size
        self._opengl_buffer = self._ctx.buffer(data=opengl_quad_array)
        self._pygame_buffer = self._ctx.buffer(data=pygame_quad_array)
        self._shader_stack = [ShaderType.BASE]

        self._vert_shaders = {}
        self._frag_shaders = {}
        self._programs = {}
        self._vaos = {}
        self._textures = {}
        self.framebuffers = {}
        self._shader_passes = {}
        
        self.load_shader(ShaderType.BASE)
        self.load_shader(ShaderType._CALIBRATE)
        self.create_framebuffer(ShaderType._CALIBRATE)

    def load_shader(self, shader_type, **kwargs):
        self._shader_passes[shader_type] = shader_pass_lookup[shader_type](self, **kwargs)

        self.create_vao(shader_type)
    
    def clear_shaders(self):
        self._shader_stack = [ShaderType.BASE]
    
    def create_vao(self, shader_type):
        frag_name = shader_type[1:] if shader_type[0] == '_' else shader_type
        vert_path = Path(shader_path / 'vertex/base.vert').resolve()
        frag_path = Path(shader_path / f'fragments/{frag_name}.frag').resolve()

        self._vert_shaders[shader_type] = vert_path.read_text()
        self._frag_shaders[shader_type] = frag_path.read_text()
        
        program = self._ctx.program(vertex_shader=self._vert_shaders[shader_type], fragment_shader=self._frag_shaders[shader_type])
        self._programs[shader_type] = program
        
        if shader_type == ShaderType._CALIBRATE:
            self._vaos[shader_type] = self._ctx.vertex_array(self._programs[shader_type], [(self._pygame_buffer, '2f 2f', 'vert', 'texCoords')])
        else:
            self._vaos[shader_type] = self._ctx.vertex_array(self._programs[shader_type], [(self._opengl_buffer, '2f 2f', 'vert', 'texCoords')])
    
    def create_framebuffer(self, shader_type, size=None, filter=moderngl.NEAREST):
        texture_size = size or self._screen_size
        texture = self._ctx.texture(size=texture_size, components=4)
        texture.filter = (filter, filter)

        self._textures[shader_type] = texture
        self.framebuffers[shader_type] = self._ctx.framebuffer(color_attachments=[self._textures[shader_type]])
    
    def render_to_fbo(self, shader_type, texture, output_fbo=None, program_type=None, use_image=True, **kwargs):
        fbo = output_fbo or self.framebuffers[shader_type]
        program = self._programs[program_type] if program_type else self._programs[shader_type]
        vao= self._vaos[program_type] if program_type else self._vaos[shader_type]

        fbo.use()
        texture.use(0)

        if use_image:
            program['image'] = 0
        for uniform, value in kwargs.items():
            program[uniform] = value
            
        vao.render(mode=moderngl.TRIANGLE_STRIP)
    
    def apply_shader(self, shader_type, **kwargs):
        if shader_type in self._shader_stack:
            return
            raise ValueError('(ShaderManager) Shader already being applied!', shader_type)
        
        self.load_shader(shader_type, **kwargs)
        self._shader_stack.append(shader_type)

        self._shader_stack.sort(key=lambda shader: -SHADER_PRIORITY.index(shader))
    
    def remove_shader(self, shader_type):
        if shader_type in self._shader_stack:
            self._shader_stack.remove(shader_type)
    
    def render_output(self, texture):
        output_shader_type = self._shader_stack[-1]
        self._ctx.screen.use() # IMPORTANT
        
        self.get_fbo_texture(output_shader_type).use(0)
        self._programs[output_shader_type]['image'] = 0

        self._vaos[output_shader_type].render(mode=moderngl.TRIANGLE_STRIP) # SOMETHING ABOUT DRAWING FLIPS THE

    def get_fbo_texture(self, shader_type):
        return self.framebuffers[shader_type].color_attachments[0]
    
    def calibrate_pygame_surface(self, pygame_surface):
        texture = self._ctx.texture(pygame_surface.size, 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'BGRA'
        texture.write(pygame_surface.get_view('1'))

        self.render_to_fbo(ShaderType._CALIBRATE, texture)

        return self.get_fbo_texture(ShaderType._CALIBRATE)
    
    def draw(self, surface, arguments):
        self._ctx.viewport = (0, 0, *self._screen_size)
        texture = self.calibrate_pygame_surface(surface)

        for shader_type in self._shader_stack:
            self._shader_passes[shader_type].apply(texture, **arguments.get(shader_type, {}))
            texture = self.get_fbo_texture(shader_type)

        self.render_output(texture)
    
    def __del__(self):
        self.cleanup()
    
    def cleanup(self):
        self._pygame_buffer.release()
        self._opengl_buffer.release()
        for program in self._programs:
            self._programs[program].release()
        for texture in self._textures:
            self._textures[texture].release()
        for vao in self._vaos:
            self._vaos[vao].release()
        for framebuffer in self.framebuffers:
            self.framebuffers[framebuffer].release()
    
    def handle_resize(self, new_screen_size):
        self._screen_size = new_screen_size

        for shader_type in self.framebuffers:
            filter = self._textures[shader_type].filter[0]
            self.create_framebuffer(shader_type, size=self._screen_size, filter=filter) # RECREATE FRAMEBUFFER TO PREVENT SCALING ISSUES