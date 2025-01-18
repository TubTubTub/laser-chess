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
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.MAIN, texture, image=0)

class Grayscale:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.GRAYSCALE)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.GRAYSCALE, texture, image=0)

class CRT:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.CRT)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.CRT, texture, image=0)

class Bloom:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.BLOOM)
        shader_manager.create_framebuffer(ShaderType.BLUR)
        shader_manager.create_framebuffer(ShaderType.HIGHLIGHT)
    
    def apply(self, texture, output_fbo):
        Highlight(self._shader_manager).apply(texture)
        Blur(self._shader_manager).apply(self._shader_manager.get_fbo_texture(ShaderType.HIGHLIGHT))
        
        self._shader_manager.get_fbo_texture(ShaderType.BLUR).use(1)
        self._shader_manager.render_to_fbo(ShaderType.BLOOM, texture, image=0, blurredImage=1)

class Highlight:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.HIGHLIGHT)
    
    def apply(self, texture):
        self._shader_manager.render_to_fbo(ShaderType.HIGHLIGHT, texture, threshold=BLOOM_THRESHOLD, intensity=BLOOM_INTENSITY)

class Blur:
    def __init__(self, shader_manager):
        self._shader_manager = shader_manager

        shader_manager.create_framebuffer(ShaderType.BLUR)

        shader_manager.create_framebuffer("blurPing")
        shader_manager.create_framebuffer("blurPong")
    
    def apply(self, texture):
        self._shader_manager.get_fbo_texture("blurPong").write(texture.read())

        for _ in range(BLUR_ITERATIONS):
            self._shader_manager.render_to_fbo(
                ShaderType.BLUR,
                texture=self._shader_manager.get_fbo_texture("blurPong"),
                output_fbo=self._shader_manager.framebuffers["ping"],
                image=0,
                passes=5,
                horizontal=True
            )
            self._shader_manager.render_to_fbo(
                ShaderType.BLUR,
                texture=self._shader_manager.get_fbo_texture("blurping"),
                output_fbo=self._shader_manager.framebuffers["pong"],
                image=0,
                passes=5,
                horizontal=False
            )

        self._shader_manager.render_to_fbo(ShaderType.BLUR, self._shader_manager.get_fbo_texture("blurPong"), image=0)

shader_pass_lookup = {
    ShaderType.MAIN: Main,
    ShaderType.BLOOM: Bloom,
    ShaderType.BLUR: Blur,
    ShaderType.HIGHLIGHT: Highlight,
    ShaderType.GRAYSCALE: Grayscale,
    ShaderType.CRT: CRT,
}

class ShaderManager:
    def __init__(self, ctx: moderngl.Context, screen_size):
        self._ctx = ctx
        self._screen_size = screen_size
        self._buffer = self._ctx.buffer(data=quad_array)
        self._shader_stack = [ShaderType.MAIN]

        self._vert_shaders = {}
        self._frag_shaders = {}
        self._programs = {}
        self._vaos = {}
        self._textures = {}
        self.framebuffers = {}
        self._shader_passes = {}

        self.load_shader(ShaderType.MAIN)

    def load_shader(self, shader_type):
        self._shader_passes[shader_type] = shader_pass_lookup[shader_type](self)

        vert_path = Path(shader_path / 'main.vert').resolve()
        frag_path = Path(shader_path / (shader_type + '.frag')).resolve()

        self._vert_shaders[shader_type] = vert_path.read_text()
        self._frag_shaders[shader_type] = frag_path.read_text()

        self.create_vao(shader_type)
    
    def create_vao(self, shader_type):
        program = self._ctx.program(vertex_shader=self._vert_shaders[shader_type], fragment_shader=self._frag_shaders[shader_type])
        self._programs[shader_type] = program
        self._vaos[shader_type] = self._ctx.vertex_array(self._programs[shader_type], [(self._buffer, '2f 2f', 'vert', 'texCoords')])

    def create_texture(self, shader_type):
        texture = self._ctx.texture(size=self._screen_size, components=4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self._textures[shader_type] = texture
    
    def create_framebuffer(self, shader_type):
        self.create_texture(shader_type)
        self.framebuffers[shader_type] = self._ctx.framebuffer(color_attachments=[self._textures[shader_type]])
    
    def render_to_fbo(self, shader_type, texture, output_fbo=None, **kwargs):
        fbo = output_fbo or self.framebuffers[shader_type]
        fbo.use()
        texture.use(0)
        
        self._programs[shader_type].__dict__.update(kwargs)

        self._vaos[shader_type].render(mode=moderngl.TRIANGLE_STRIP)
    
    def apply_shader(self, shader_type):
        if shader_type in self._shader_stack:
            raise ValueError('(ShaderManager) Shader already being applied!', shader_type)
        
        self.load_shader(shader_type)
        self._shader_stack.insert(-1, shader_type) # ShaderType.MAIN always last
    
    def remove_shader(self, shader_type):
        self._shader_stack.remove(shader_type)
    
    def render_main(self):
        self._ctx.screen.use() # IMPORTANT
        self.get_fbo_texture(ShaderType.MAIN).use(0)
        self._programs[ShaderType.MAIN]['image'] = 0
        self._vaos[ShaderType.MAIN].render(mode=moderngl.TRIANGLE_STRIP)
    
    def get_fbo_texture(self, shader_type):
        return self.framebuffers[shader_type].color_attachments[0]

    def draw(self, screen_texture):
        texture = screen_texture

        for shader_type in self._shader_stack:
            self._shader_passes[shader_type].apply(texture)
            texture = self.get_fbo_texture(shader_type)

        screen_texture.release()
        self.render_main()
    
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