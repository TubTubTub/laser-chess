import pygame
from data.constants import ShaderType
from data.shaders.protocol import SMProtocol

class Base:
    def __init__(self, shader_manager: SMProtocol):
        self._shader_manager = shader_manager

        self._shader_manager.create_framebuffer(ShaderType.BASE)
        self._shader_manager.create_vao(ShaderType.BACKGROUND_WAVES)
        self._shader_manager.create_vao(ShaderType.BACKGROUND_BALATRO)
        self._shader_manager.create_vao(ShaderType.BACKGROUND_LASERS)
        self._shader_manager.create_vao(ShaderType.BACKGROUND_GRADIENT)
        self._shader_manager.create_vao(ShaderType.BACKGROUND_NONE)
    
    def apply(self, texture, background_type=None):
        base_texture = self._shader_manager.get_fbo_texture(ShaderType.BASE)
        
        match background_type:
            case ShaderType.BACKGROUND_WAVES:
                self._shader_manager.render_to_fbo(
                    ShaderType.BASE,
                    texture=base_texture,
                    program_type=ShaderType.BACKGROUND_WAVES,
                    use_image=False,
                    time=pygame.time.get_ticks() / 1000
                )
            case ShaderType.BACKGROUND_BALATRO:
                self._shader_manager.render_to_fbo(
                    ShaderType.BASE,
                    texture=base_texture,
                    program_type=ShaderType.BACKGROUND_BALATRO,
                    use_image=False,
                    time=pygame.time.get_ticks() / 1000,
                    screenSize=base_texture.size
                )
            case ShaderType.BACKGROUND_LASERS:
                self._shader_manager.render_to_fbo(
                    ShaderType.BASE,
                    texture=base_texture,
                    program_type=ShaderType.BACKGROUND_LASERS,
                    use_image=False,
                    time=pygame.time.get_ticks() / 1000,
                   screenSize=base_texture.size
                )
            case ShaderType.BACKGROUND_GRADIENT:
                self._shader_manager.render_to_fbo(
                    ShaderType.BASE,
                    texture=base_texture,
                    program_type=ShaderType.BACKGROUND_GRADIENT,
                    use_image=False,
                    time=pygame.time.get_ticks() / 1000,
                   screenSize=base_texture.size
                )
            case None:
                self._shader_manager.render_to_fbo(
                    ShaderType.BASE,
                    texture=base_texture,
                    program_type=ShaderType.BACKGROUND_NONE,
                    use_image=False,
                )
            case _:
                raise ValueError('(shader.py) Unknown background type:', background_type)

        self._shader_manager.get_fbo_texture(ShaderType.BASE).use(1)
        self._shader_manager.render_to_fbo(ShaderType.BASE, texture, background=1)