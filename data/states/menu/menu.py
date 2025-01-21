import pygame
from data.control import _State
from data.components.widget_group import WidgetGroup
from data.states.menu.widget_dict import MENU_WIDGETS
from data.constants import MenuEventType
from data.components.cursor import Cursor
from data.assets import GRAPHICS, MUSIC_PATHS
from data.utils.asset_helpers import draw_background
from data.managers.audio import audio
from data.managers.animation import animation
from data.managers.window import screen
from data.utils.asset_helpers import get_rotational_angle
import math

class Menu(_State):
    def __init__(self):
        super().__init__()
        self._cursor = Cursor()
        
        self._widget_group = None
    
    def cleanup(self):
        print('cleaning menu.py')

        return None
    
    def startup(self, persist=None):
        print('starting menu.py')
        self._widget_group = WidgetGroup(MENU_WIDGETS)
        self._widget_group.handle_resize(screen.size)

        audio.play_music(MUSIC_PATHS['menu'])

        self.draw()
    
    def get_event(self, event):
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
    
    def handle_resize(self):
        self._widget_group.handle_resize(screen.get_size())

    
    def draw_sphinx(self):
        mouse_pos = (pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1] + 0.1)
        sphinx_size = (min(screen.size) * 0.1, min(screen.size) * 0.1)
        sphinx_position = (screen.size[0] - sphinx_size[0], screen.size[1] - sphinx_size[1])

        sphinx_center = (sphinx_position[0] + sphinx_size[0] / 2, sphinx_position[1] + sphinx_size[1] / 2)
        sphinx_rotation = -get_rotational_angle(mouse_pos, sphinx_center) - 30

        sphinx_surface = pygame.transform.scale(GRAPHICS['sphinx_1'], sphinx_size)
        sphinx_surface = pygame.transform.rotate(sphinx_surface, sphinx_rotation)

        screen.blit(sphinx_surface, sphinx_position)
    
    def draw_mask(self, surface):
        mask = pygame.mask.from_surface(surface, threshold=254)
        screen.blit(mask.to_surface(unsetcolor=(0, 0, 0, 0), setcolor=(255, 255, 255, 255)), ((0, 0)))
    
    def draw(self):
        # draw_background(screen, GRAPHICS['temp_background'])

        # temp_surface = pygame.Surface((screen.size[0] / 2, screen.size[1] / 2), pygame.SRCALPHA)
        # temp_surface.fill((0, 0, 0, 0))
        screen.fill((0, 0, 10, 255))
        self._widget_group.draw()
        self.draw_sphinx()
        pygame.draw.rect(screen, 'red', (100, 100, 100, 100))

        # self.draw_mask(screen)
    
    def update(self, **kwargs):
        self.draw()