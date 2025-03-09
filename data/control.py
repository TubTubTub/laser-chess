import pygame
from data.components.widget_group import WidgetGroup
from data.managers.logs import initialise_logger
from data.managers.cursor import CursorManager
from data.managers.animation import animation
from data.utils.assets import DEFAULT_FONT
from data.managers.window import window
from data.managers.audio import audio
from data.managers.theme import theme

logger = initialise_logger(__file__)

FPS = 60
SHOW_FPS = False
start_ticks = pygame.time.get_ticks()

class Control:
    def __init__(self):
        self.done = False
        self._clock = pygame.time.Clock()

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state

        self.state = self.state_dict[self.state_name]
        self.state.startup()

    def flip_state(self):
        self.state.done = False
        persist = self.state.cleanup()

        previous, self.state_name = self.state_name, self.state.next

        self.state = self.state_dict[self.state_name]
        self.state.previous = previous
        self.state.startup(persist)

    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()

        self._clock.tick(FPS)
        animation.set_delta_time()

        self.state.update()

        if SHOW_FPS:
            self.draw_fps()

        window.update()

    def main_game_loop(self):
        while not self.done:
            self.event_loop()
            self.update()

    def update_window(self, resize=False):
        if resize:
            self.update_native_window_size()
            window.handle_resize()
            self.state.handle_resize()

        self.update()

    def draw_fps(self):
        fps = str(int(self._clock.get_fps()))
        DEFAULT_FONT.strength = 0.1
        DEFAULT_FONT.render_to(window.screen, (0, 0), fps, fgcolor=theme['textError'], size=15)

    def update_native_window_size(self):
        x, y = window.size

        max_window_x = 100000
        max_window_y = x / 1.4
        min_window_x = 400
        min_window_y = min_window_x/1.4

        if x / y < 1.4:
            min_window_x = x

        min_window_size = (min_window_x, min_window_y)
        max_window_size = (max_window_x, max_window_y)
        window.minimum_size = min_window_size
        window.maximum_size = max_window_size

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True

            if event.type == pygame.MOUSEBUTTONDOWN and event.button != 1: # ONLY PROCESS LEFT CLICKS
                return

            self.state.get_event(event)

class _State:
    def __init__(self):
        self.next = None
        self.previous = None
        self.done = False
        self.quit = False
        self.persist = {}

        self._cursor = CursorManager()
        self._widget_group = None

    def startup(self, widgets=None, music=None):
        if widgets:
            self._widget_group = WidgetGroup(widgets)
            self._widget_group.handle_resize(window.size)

        if music:
            audio.play_music(music)

        logger.info(f'starting {self.__class__.__name__.lower()}.py')

    def cleanup(self):
        logger.info(f'cleaning {self.__class__.__name__.lower()}.py')

    def draw(self):
        raise NotImplementedError

    def get_event(self, event):
        raise NotImplementedError

    def handle_resize(self):
        self._widget_group.handle_resize(window.size)

    def update(self, **kwargs):
        self.draw()