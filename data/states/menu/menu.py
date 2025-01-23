import pygame
from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.menu.widget_dict import MENU_WIDGETS
from data.constants import MenuEventType, ShaderType
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import draw_background
from data.managers.audio import audio
from data.managers.animation import animation
from data.managers.window import window
from data.utils.asset_helpers import get_rotational_angle
from random import randint

class Menu(_State):
    def __init__(self):
        super().__init__()
        self._fire_laser = False

    @property
    def sphinx_center(self):
        return (window.size[0] - self.sphinx_size[0] / 2, window.size[1] - self.sphinx_size[1] / 2)
    
    @property
    def sphinx_size(self):
        return (min(window.size) * 0.1, min(window.size) * 0.1)

    @property
    def sphinx_rotation(self):
        mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 0.01)
        return -get_rotational_angle(mouse_pos, self.sphinx_center)
    
    def cleanup(self):
        print('cleaning menu.py')

        return None
    
    def startup(self, persist=None):
        print('starting menu.py')
        self._widget_group = WidgetGroup(MENU_WIDGETS)
        self._widget_group.handle_resize(window.size)
        self._fire_laser = False

        audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def get_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._fire_laser = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self._fire_laser = False
            window.clear_effect(ShaderType.RAYS)
            
        widget_event = self._widget_group.process_event(event)

        if widget_event is None:
            return

        match widget_event.type:
            case None:
                return

            case MenuEventType.CONFIG_CLICK:
                self.next = 'config'
                self.done = True
            case MenuEventType.SETTINGS_CLICK:
                self.next = 'settings'
                self.done = True
            case MenuEventType.BROWSER_CLICK:
                self.next = 'browser'
                self.done = True
    
    def draw_sphinx(self):
        sphinx_surface = pygame.transform.scale(GRAPHICS['sphinx_1'], self.sphinx_size)
        sphinx_surface = pygame.transform.rotate(sphinx_surface, self.sphinx_rotation - 30)
        sphinx_rect = pygame.FRect(0, 0, *self.sphinx_size)
        sphinx_rect.center = self.sphinx_center

        window.screen.blit(sphinx_surface, sphinx_rect)
    
    def draw(self):
        # draw_background(window.screen, GRAPHICS['temp_background'])
        
        window.screen.fill((0, 0, 0, 0))
        self._widget_group.draw()
        self.draw_sphinx()
        window.set_apply_arguments(ShaderType.BLOOM, occlusion_surface=window.screen, occlusion_intensity=0.7)
    
    def update(self, **kwargs):
        if self._fire_laser:
            window.clear_effect(ShaderType.RAYS)
            
            window.set_effect(ShaderType.RAYS, lights=[[
                (self.sphinx_center[0] / window.size[0], self.sphinx_center[1] / window.size[1]),
                2.2,
                (230, 230, 255),
                0.99,
                (self.sphinx_rotation - 2 + randint(-5, 5) / 40, self.sphinx_rotation + 2 + randint(-5, 5) / 40)
            ]])

        super().update(**kwargs)