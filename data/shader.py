from data.constants import ShaderType
from array import array
from pathlib import Path
import moderngl

shader_path = (Path(__file__).parent / './shaders/').resolve()

quad_array = array('f', [
    -1.0, 1.0, 0.0, 0.0,
    1.0, 1.0, 1.0, 0.0,
    -1.0, -1.0, 0.0, 1.0,
    1.0, -1.0, 1.0, 1.0,
])

BLOOM_THRESHOLD = 1.0
BLOOM_INTENSITY = 1.0
BLUR_ITERATIONS = 1.0

class Main:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType.MAIN)
    
    def apply(self, texture, output_fbo=None):
        texture.use()
        self._shader_manager.render_to_fbo(ShaderType.MAIN)
        # output_fbo.color_attachments[0].write(data=self._shader_manager.framebuffers[ShaderType.MAIN].color_attachments[0].read())
        texture.release()

class Grayscale:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.GRAYSCALE)
    
    def apply(self, texture, output_fbo):
        texture.use()
        self._shader_manager.render_to_fbo(ShaderType.GRAYSCALE)
        output_fbo.write(self._shader_manager.get_fbo_attachment(ShaderType.GRAYSCALE).read())

class Bloom:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager


        shader_manager.create_framebuffer(ShaderType.BLOOM)
        shader_manager.create_framebuffer(ShaderType.BLUR)
        shader_manager.create_framebuffer(ShaderType.CONTRAST)
    
    def apply(self, texture, output_fbo):
        Contrast(self._shader_manager).apply(texture)
        Blur(self._shader_manager).apply(self._shader_manager.get_fbo_attachment(ShaderType.CONTRAST))
        
        texture.use(0)
        self._shader_manager.use_framebuffer(ShaderType.BLUR, location=1)
        self._shader_manager.render_to_fbo(ShaderType.BLOOM, uTexture=0, uBlur=1)

        output_fbo.write(self._shader_manager.get_fbo_attachment(ShaderType.BLOOM).read())

class Contrast:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.CONTRAST)
    
    def apply(self, texture, output_fbo=None):
        output_fbo = output_fbo or self._shader_manager.framebuffers[ShaderType.CONTRAST]

        texture.use()
        self._shader_manager.render_to_fbo(ShaderType.CONTRAST, uThreshold=BLOOM_THRESHOLD, uIntensity=BLOOM_INTENSITY)
        output_fbo.write(self._shader_manager.get_fbo_attachment(ShaderType.CONTRAST).read())

class Blur:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.load_shader(ShaderType.BLUR)

        shader_manager.create_framebuffer("ping" )
        shader_manager.create_framebuffer("pong" )
    
    def apply(self, texture, output_fbo=None):
        output_fbo = output_fbo or self._shader_manager.framebuffers[ShaderType.BLUR]

        self._shader_manager._textures["ping"].write(texture.read())

        for _ in range(BLUR_ITERATIONS):
            self._shader_manager.use_framebuffer("ping")

            self._shader_manager.render_to_fbo(ShaderType.BLUR, output_fbo=self._shader_manager.framebuffers["pong"])
            self._shader_manager.use_framebuffer("pong")

            self._shader_manager.render_to_fbo(ShaderType.BLUR, output_fbo=self._shader_manager.framebuffers["ping"])
        
        output_fbo.write(self._shader_manager.get_fbo_attachment("pong").read())

shader_pass_lookup = {
    ShaderType.MAIN: Main,
    ShaderType.BLOOM: Bloom,
    ShaderType.BLUR: Blur,
    ShaderType.CONTRAST: Contrast,
    ShaderType.GRAYSCALE: Grayscale,
}

class ShaderManager:
    def __init__(self, ctx: moderngl.Context, screen_size):
        self._ctx = ctx
        self._screen_size = screen_size
        self._buffer = self._ctx.buffer(data=quad_array)
        self._shader_stack = []

        self._vert_shaders = {}
        self._frag_shaders = {}
        self._programs = {}
        self._vaos = {}
        self._textures = {}
        self.framebuffers = {}
        self._shader_passes = {}

    def load_shader(self, shader_type):
        print('Loading shader:', shader_type)
        self._shader_passes[shader_type] = shader_pass_lookup[shader_type](self)

        vert_path = Path(shader_path / (shader_type + '.vert')).resolve()
        frag_path = Path(shader_path / (shader_type + '.frag')).resolve()

        self._vert_shaders[shader_type] = vert_path.read_text()
        self._frag_shaders[shader_type] = frag_path.read_text()

        self.create_vao(shader_type)
    
    def create_vao(self, shader_type):
        print('Creating vao:', shader_type)
        program = self._ctx.program(vertex_shader=self._vert_shaders[shader_type], fragment_shader=self._frag_shaders[shader_type])
        self._programs[shader_type] = program
        self._vaos[shader_type] = self._ctx.vertex_array(program, [(self._buffer, '2f 2f', 'vert', 'texCoords')])

    def create_texture(self, shader_type):
        texture = self._ctx.texture(size=self._screen_size, components=4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'BGRA' # MAYBE DON'T NEED

        self._textures[shader_type] = texture
    
    def create_framebuffer(self, shader_type):
        self.create_texture(shader_type)
        framebuffer = self._ctx.framebuffer(color_attachments=self._textures[shader_type])
        self.framebuffers[shader_type] = framebuffer
    
    def use_framebuffer(self, shader_type, attachment=0, location=0):
        self.framebuffers[shader_type].color_attachments[attachment].use(location)
    
    def get_fbo_attachment(self, shader_type):
        return self.framebuffers[shader_type].color_attachments[0]
    
    def render_to_fbo(self, shader_type, program=None, vao=None, output_fbo=None, **kwargs):
        fbo = output_fbo or self.framebuffers[shader_type]
        vao = vao or self._vaos[shader_type]
        program = program or shader_type

        self._textures[shader_type].use()
        # fbo.use() NOT WORKING IF THIS TURNED ON
        
        # self._programs[program].__dict__.update(kwargs)
        for uniform in kwargs:
            self._programs[program][uniform] = kwargs[uniform]

        vao.render(mode=moderngl.TRIANGLE_STRIP)
        print(self._programs[ShaderType.MAIN] == self._programs[program],uniform)
    
    def apply_shader(self, shader_type):
        if shader_type in self._shader_stack:
            raise ValueError('(ShaderManager) Shader already being applied!', shader_type)
        
        self.load_shader(shader_type)
        self._shader_stack.append(shader_type)
    
    def remove_shader(self, shader_type):
        self._shader_stack.remove(shader_type)
    
    def render_main(self):
        self._textures[ShaderType.MAIN].use(0)
        self._programs[ShaderType.MAIN]['screenTexture'] = 0
        self._vaos[ShaderType.MAIN].render(mode=moderngl.TRIANGLE_STRIP)

    def draw(self, screen_texture):
        texture = screen_texture

        self._textures[ShaderType.MAIN] = screen_texture

        # for shader_type in self._shader_stack:
        #     self._shader_passes[shader_type].apply(texture, output_fbo=self.framebuffers[shader_type])
        #     texture = self.get_fbo_attachment(shader_type)
        
        # self.render_main()
        self.render_to_fbo(ShaderType.MAIN, screenTexture=0)
    
    def __del__(self):
        self.cleanup()
    
    def cleanup(self):
        self._buffer.release()
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