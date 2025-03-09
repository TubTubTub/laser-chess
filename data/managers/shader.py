from pathlib import Path
from array import array
import moderngl
from data.shaders.classes import shader_pass_lookup
from data.shaders.protocol import SMProtocol
from data.utils.constants import ShaderType

shader_path = (Path(__file__).parent / '../shaders/').resolve()

SHADER_PRIORITY = [
    ShaderType.CRT,
    ShaderType.SHAKE,
    ShaderType.BLOOM,
    ShaderType.CHROMATIC_ABBREVIATION,
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
        self._shader_list = [ShaderType.BASE]

        self._vert_shaders = {}
        self._frag_shaders = {}
        self._programs = {}
        self._vaos = {}
        self._textures = {}
        self._shader_passes = {}
        self.framebuffers = {}

        self.load_shader(ShaderType.BASE)
        self.load_shader(ShaderType._CALIBRATE)
        self.create_framebuffer(ShaderType._CALIBRATE)

    def load_shader(self, shader_type, **kwargs):
        """
        Loads a given shader by creating a VAO reading the corresponding .frag file.

        Args:
            shader_type (ShaderType): The type of shader to load.
            **kwargs: Additional arguments passed when initialising the fragment shader class.
        """
        self._shader_passes[shader_type] = shader_pass_lookup[shader_type](self, **kwargs)
        self.create_vao(shader_type)

    def clear_shaders(self):
        """
        Clears the shader list, leaving only the base shader.
        """
        self._shader_list = [ShaderType.BASE]

    def create_vao(self, shader_type):
        """
        Creates a vertex array object (VAO) for the given shader type.

        Args:
            shader_type (ShaderType): The type of shader.
        """
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
        """
        Creates a framebuffer for the given shader type.

        Args:
            shader_type (ShaderType): The type of shader.
            size (tuple[int, int], optional): The size of the framebuffer. Defaults to screen size.
            filter (moderngl.Filter, optional): The texture filter. Defaults to NEAREST.
        """
        texture_size = size or self._screen_size
        texture = self._ctx.texture(size=texture_size, components=4)
        texture.filter = (filter, filter)

        self._textures[shader_type] = texture
        self.framebuffers[shader_type] = self._ctx.framebuffer(color_attachments=[self._textures[shader_type]])

    def render_to_fbo(self, shader_type, texture, output_fbo=None, program_type=None, use_image=True, **kwargs):
        """
        Applies the shaders and renders the resultant texture to a framebuffer object (FBO).

        Args:
            shader_type (ShaderType): The type of shader.
            texture (moderngl.Texture): The texture to render.
            output_fbo (moderngl.Framebuffer, optional): The output framebuffer. Defaults to None.
            program_type (ShaderType, optional): The program type. Defaults to None.
            use_image (bool, optional): Whether to use the image uniform. Defaults to True.
            **kwargs: Additional uniforms for the fragment shader.
        """
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
        """
        Applies a shader of the given type and adds it to the list.

        Args:
            shader_type (ShaderType): The type of shader to apply.

        Raises:
            ValueError: If the shader is already being applied.
        """
        if shader_type in self._shader_list:
            return

        self.load_shader(shader_type, **kwargs)
        self._shader_list.append(shader_type)

        # Sort shader list based on the order in SHADER_PRIORITY, so that more important shaders are applied first
        self._shader_list.sort(key=lambda shader: -SHADER_PRIORITY.index(shader))

    def remove_shader(self, shader_type):
        """
        Removes a shader of the given type from the list.

        Args:
            shader_type (ShaderType): The type of shader to remove.
        """
        if shader_type in self._shader_list:
            self._shader_list.remove(shader_type)

    def render_output(self):
        """
        Renders the final output to the screen.
        """
        # Render to the screen framebuffer
        self._ctx.screen.use()

        # Take the texture of the last framebuffer to be rendered to, and render that to the screen framebuffer
        output_shader_type = self._shader_list[-1]
        self.get_fbo_texture(output_shader_type).use(0)
        self._programs[output_shader_type]['image'] = 0

        self._vaos[output_shader_type].render(mode=moderngl.TRIANGLE_STRIP)

    def get_fbo_texture(self, shader_type):
        """
        Gets the texture from the specified shader type's FBO.

        Args:
            shader_type (ShaderType): The type of shader.

        Returns:
            moderngl.Texture: The texture from the FBO.
        """
        return self.framebuffers[shader_type].color_attachments[0]

    def calibrate_pygame_surface(self, pygame_surface):
        """
        Converts the Pygame window surface into an OpenGL texture.

        Args:
            pygame_surface (pygame.Surface): The finished Pygame surface.

        Returns:
            moderngl.Texture: The calibrated texture.
        """
        texture = self._ctx.texture(pygame_surface.size, 4)
        texture.filter = (moderngl.NEAREST, moderngl.NEAREST)
        texture.swizzle = 'BGRA'
        # Take the Pygame surface's pixel array and draw it to the new texture
        texture.write(pygame_surface.get_view('1'))

        # ShaderType._CALIBRATE has a VAO containing the pygame_quad_array coordinates, as Pygame uses different texture coordinates than ModernGL textures
        self.render_to_fbo(ShaderType._CALIBRATE, texture)
        return self.get_fbo_texture(ShaderType._CALIBRATE)

    def draw(self, surface, arguments):
        """
        Draws the Pygame surface with shaders applied to the screen.

        Args:
            surface (pygame.Surface): The final Pygame surface.
            arguments (dict): A dict of { ShaderType: Args } items, containing keyword arguments for every fragment shader.
        """
        self._ctx.viewport = (0, 0, *self._screen_size)
        texture = self.calibrate_pygame_surface(surface)

        for shader_type in self._shader_list:
            self._shader_passes[shader_type].apply(texture, **arguments.get(shader_type, {}))
            texture = self.get_fbo_texture(shader_type)

        self.render_output()

    def __del__(self):
        """
        Cleans up ModernGL resources when the ShaderManager object is deleted.
        """
        self.cleanup()

    def cleanup(self):
        """
        Cleans up resources used by the ModernGL.
        Probably unnecessary as the 'auto' garbage collection mode is used.
        """
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
        """
        Handles resizing of the screen.

        Args:
            new_screen_size (tuple[int, int]): The new screen size.
        """
        self._screen_size = new_screen_size

        # Recreate all framebuffers to prevent scaling issues
        for shader_type in self.framebuffers:
            filter = self._textures[shader_type].filter[0]
            self.create_framebuffer(shader_type, size=self._screen_size, filter=filter)