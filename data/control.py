import pygame
from data.components.animation import animation
from data.window import window

screen = window.get_surface()

FPS = 60
start_ticks = pygame.time.get_ticks()

class Control:
    def __init__(self):
        self.done = False
        self.clock = pygame.time.Clock()
        """temp for fps display counter"""
        self.font = pygame.font.SysFont("Arial" , 18 , bold=True)
        self._int = '0'
    
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

        self.clock.tick(FPS)
        animation.set_delta_time()

        self.state.update()

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
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"), True)
        screen.blit(fps_t,(0,0))
    
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
            
            self.state.get_event(event)

class _State:
    def __init__(self):
        self.next = None
        self.previous = None
        self.done = False
        self.quit = False
        self.persist = {}
    
    def draw(self, screen):
        raise NotImplementedError
    
    def update(self, **kwargs):
        raise NotImplementedError

    def handle_resize(self):
        raise NotImplementedError
    
    def get_event(self, event):
        raise NotImplementedError