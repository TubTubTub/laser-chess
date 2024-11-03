import pygame
from pygame._sdl2 import Window
from data.components.animation import animation

FPS = 60

class Control:
    def __init__(self):
        self.done = False
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        """temp for fps display counter"""
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
    
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

        current_time = pygame.time.get_ticks()
        delta_time = self.clock.tick(FPS) / 1000.0

        self.state.update()
        animation.set_current_ms(current_time)
        
        self.draw_fps()
        pygame.display.update()

    def main_game_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
    
    def update_window(self, resize=False):
        if resize:
            self.update_native_window_size()
            self.state.handle_resize()
        self.update()
    
    def draw_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"), True)
        self.screen.blit(fps_t,(0,0))
    
    def update_native_window_size(self):
        x, y = self.screen.get_rect().size

        max_screen_x = 100000
        max_screen_y = x / 1.4
        min_screen_x = 400
        min_screen_y = min_screen_x/1.4

        if x / y < 1.4:
            min_screen_x = x

        min_screen_size = (min_screen_x, min_screen_y)
        max_screen_size = (max_screen_x, max_screen_y)
        Window.from_display_module().minimum_size = min_screen_size
        Window.from_display_module().maximum_size = max_screen_size
    
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