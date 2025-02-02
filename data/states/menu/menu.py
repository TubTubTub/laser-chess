import pygame
import sys
from random import randint

from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.menu.widget_dict import MENU_WIDGETS
from data.constants import MenuEventType, ShaderType
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import scale_and_cache
from data.managers.audio import audio
from data.managers.window import window
from data.managers.animation import animation
from data.utils.asset_helpers import get_rotational_angle
from data.managers.logs import initialise_logger

logger = initialise_logger(__file__)

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
        logger.info('cleaning menu.py')
        window.clear_apply_arguments(ShaderType.BLOOM)
        window.clear_apply_arguments(ShaderType.SHAKE)
        return None
    
    def startup(self, persist=None):
        logger.info('starting menu.py')
        window.set_apply_arguments(ShaderType.BASE, background_type=ShaderType._BACKGROUND_BALATRO)
        self._widget_group = WidgetGroup(MENU_WIDGETS)
        self._widget_group.handle_resize(window.size)
        MENU_WIDGETS['credits'].kill()
        self._fire_laser = False

        audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def get_event(self, event):
        if event.type in [pygame.MOUSEBUTTONUP, pygame.KEYDOWN]:
            MENU_WIDGETS['credits'].kill()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._fire_laser = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self._fire_laser = False
            window.clear_effect(ShaderType.RAYS)
            animation.set_timer(300, lambda: window.clear_effect(ShaderType.SHAKE))
            
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
            case MenuEventType.QUIT_CLICK:
                pygame.quit()
                sys.exit()
                print('quitting...')
            case MenuEventType.CREDITS_CLICK:
                self._widget_group.add(MENU_WIDGETS['credits'])
    
    def draw_sphinx(self):
        sphinx_surface = scale_and_cache(GRAPHICS['sphinx_0_b'], self.sphinx_size)
        sphinx_surface = pygame.transform.rotate(sphinx_surface, self.sphinx_rotation)
        sphinx_rect = pygame.FRect(0, 0, *self.sphinx_size)
        sphinx_rect.center = self.sphinx_center

        window.screen.blit(sphinx_surface, sphinx_rect)
    
    def draw(self):
        self._widget_group.draw()
        self.draw_sphinx()

        widget_mask = window.screen.copy()

        if self._fire_laser:
            laser_mask = pygame.mask.from_surface(widget_mask)
            laser_mask = laser_mask.to_surface(setcolor=(255, 0, 0, 255), unsetcolor=(0, 0, 0, 255))
            pygame.draw.rect(laser_mask, (0, 0, 0), (window.screen.width - self.sphinx_size[0], window.screen.height - self.sphinx_size[1], *self.sphinx_size))

            window.set_apply_arguments(ShaderType.RAYS, occlusion=laser_mask)

        pygame.draw.rect(widget_mask, (0, 0, 0, 255), (window.screen.width - 50, 0, 50, 50))
        window.set_apply_arguments(ShaderType.BLOOM, occlusion_surface=widget_mask, occlusion_intensity=0.3, brightness_intensity=0.6)
    
    def update(self, **kwargs):
        if self._fire_laser:
            window.clear_effect(ShaderType.RAYS)
            window.set_effect(ShaderType.RAYS, lights=[[
                (self.sphinx_center[0] / window.size[0], self.sphinx_center[1] / window.size[1]),
                2.2,
                (190, 190, 255),
                0.99,
                (self.sphinx_rotation - 2 + randint(-5, 5) / 40, self.sphinx_rotation + 2 + randint(-5, 5) / 40)
            ]])

            window.set_effect(ShaderType.SHAKE)
            window.set_apply_arguments(ShaderType.SHAKE, intensity=1)

        super().update(**kwargs)