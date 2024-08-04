import pygame
from pygame._sdl2 import Window

class Control:
    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.done = False
        self.screen = pygame.display.set_mode(self.size, self.screenFlags)
        self.clock = pygame.time.Clock()
    
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
    
    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup()
        self.state.previous = previous
    
    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()

        x, y = self.screen.get_rect().size

        max_screen_x = 100000
        max_screen_y = x / 1.4
        min_screen_x = 200
        min_screen_y = 200/1.4

        if x / y < 1.4:
            min_screen_x = x

        min_screen_size = (min_screen_x, min_screen_y)
        max_screen_size = (max_screen_x, max_screen_y)
        Window.from_display_module().minimum_size = min_screen_size
        Window.from_display_module().maximum_size = max_screen_size
        
        self.state.update(self.screen)
        pygame.display.update()
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
            
            self.state.get_event(event)

    def main_game_loop(self):
        while not self.done:
            self.clock.tick(self.fps)
            self.event_loop()
            self.update()

class _State:
    def __init__(self):
        self.next = None
        self.previous = None
        self.done = False
        self.quit = False