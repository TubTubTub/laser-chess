import pygame
import moderngl
from typing import Protocol, Optional
from data.constants import ShaderType

class SMProtocol(Protocol):
    def load_shader(self, shader_type: ShaderType, **kwargs) -> None: pass
    def clear_shaders(self) -> None: pass
    def create_vao(self, shader_type: ShaderType) -> None: pass
    def create_framebuffer(self, shader_type: ShaderType, size: Optional[tuple[int]]=None, filter: Optional[int]=moderngl.NEAREST) -> None: pass
    def render_to_fbo(self, shader_type: ShaderType, texture: moderngl.Texture, output_fbo: Optional[moderngl.Framebuffer] = None, program_type: Optional[ShaderType] = None, use_image: Optional[bool] = True, **kwargs) -> None: pass
    def apply_shader(self, shader_type: ShaderType, **kwargs) -> None: pass
    def remove_shader(self, shader_type: ShaderType) -> None: pass
    def render_output(self, texture: moderngl.Texture) -> None: pass
    def get_fbo_texture(self, shader_type: ShaderType) -> moderngl.Texture: pass
    def calibrate_pygame_surface(self, pygame_surface: pygame.Surface) -> moderngl.Texture: pass
    def draw(self, surface: pygame.Surface, arguments: dict) -> None: pass
    def __del__(self) -> None: pass
    def cleanup(self) -> None: pass
    def handle_resize(self, new_screen_size: tuple[int]) -> None: pass