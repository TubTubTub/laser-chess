from data.constants import ShaderType
from array import array
from pathlib import Path
import moderngl

shader_folder_path = (Path(__file__).parent / './shaders/').resolve()

quad_array = array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
])

class ShaderManager:
    def __init__(self, ctx):
        self._ctx = ctx

        self._vert_shaders = {}
        self._frag_shaders = {}
        self._programs = {}
        self._buffers = {
            ShaderType.BASE: self._ctx.buffer(data=quad_array)
        }
        self._vaos = {}
        self._vbos = {}
        self._textures = {}
        self.framebuffers = {}

        self.load_shader(ShaderType.BASE)

    def load_shader(self, shader_type):
        vert_path = Path(shader_folder_path / shader_type + '.vert').resolve()
        frag_path = Path(shader_folder_path / shader_type + '.frag').resolve()

        self._vert_shaders[shader_type] = vert_path.read_text()
        self._frag_shaders[shader_type] = frag_path.read_text()
    
    def cleanup(self):
        for program in self._programs:
            self._programs[program].release()
        for texture in self._textures:
            self._textures[texture].release()
        for vao in self._vaos:
            self._vaos[vao].release()
        for buffer in self._buffers:
            self._buffers[buffer].release()
        for framebuffer in self.framebuffers:
            self.framebuffers[framebuffer].release()
    
    def create_vao(self, shader_type):
        program = self._ctx.program(vertex_shader=self._vert_shaders[shader_type], fragment_shader=self._frag_shaders[shader_type])
        self._ctx.vertex_array(program, [(self._buffers[ShaderType.BASE], '2f 2f', 'vert', 'texCoords')])

    def create_texture(self, shader_type, size):
        texture = self._ctx.texture(size=size, components=4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'BGRA' # MAYBE DON'T NEED

        self._textures[shader_type] = texture
    
    def create_framebuffer(self, shader_type):
        framebuffer = self._ctx.framebuffer(color_attachments=self._textures[shader_type])
        self.framebuffers[shader_type] = framebuffer
    
    def __del__(self):
        self.cleanup()
    
    def apply_pass(self, shader_type, texture, output_fbo, **kwargs):
        texture.use()
        self.framebuffers[shader_type].use()
        self._programs[shader_type].__dict__.update(kwargs)

        self._vaos.render(mode=moderngl.TRIANGLE_STRIP)

        output_fbo.color_attachments[0].write(data=self.framebuffers[shader_type].color_attachments[0].read())
    
    def sample_framebuffer(self, shader_type, attachment=0, location=0):
        self.framebuffers[shader_type].color_attachments[attachment].use(location)

class Bloom:
    def __init__(self, shader_manager, texture_size):
        self._shader_manager = shader_manager

        shader_manager.load_shader(ShaderType.BLOOM)
        shader_manager.create_vao(ShaderType.BLOOM)

        shader_manager.create_texture(ShaderType.BLOOM, texture_size)
        shader_manager.create_texture(ShaderType.BLUR, texture_size)
        shader_manager.create_texture(ShaderType.CONTRAST, texture_size)

        shader_manager.create_framebuffer(ShaderType.BLOOM)
        shader_manager.create_framebuffer(ShaderType.BLUR)
        shader_manager.create_framebuffer(ShaderType.CONTRAST)
        
    
    def update(self, screen_texture, output_fbo, threshold=1.0, intensity=1.0):

        self._shader_manager.apply_pass(
            ShaderType.CONTRAST,
            screen_texture,
            self._shader_manager.framebuffers[ShaderType.CONTRAST]
        )
        self._shader_manager.apply_pass(
            ShaderType.BLUR,
            self._shader_manager.framebuffers[ShaderType.CONTRAST].color_attachments[0],
            self._shader_manager.framebuffers[ShaderType.BLUR]
        )
        
        screen_texture.use(0)
        self._shader_manager.sample_framebuffer(ShaderType.BLUR, location=1)
        self._shader_manager.apply_pass(ShaderType.BLOOM, self._shader_manager.framebuffers[ShaderType.BLUR].color_attachments[0], output_fbo)