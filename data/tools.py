import pygame
from pygame._sdl2 import Window
from pathlib import Path
from functools import cache

class Control:
    def __init__(self):
        self.done = False
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.fps = 60
        """temp"""
        self.font = pygame.font.SysFont("Arial" , 18 , bold = True)
    
    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state_name = start_state
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.screen)
    
    def flip_state(self):
        self.state.done = False
        previous, self.state_name = self.state_name, self.state.next
        self.state.cleanup()
        self.state = self.state_dict[self.state_name]
        self.state.startup(self.screen)
        self.state.previous = previous
    
    def update(self):
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        
        self.draw_fps()
        
        self.state.update()
        pygame.display.update()

    def main_game_loop(self):
        while not self.done:
            self.clock.tick(self.fps)
            self.event_loop()
            self.update()
    
    def resize_window_event(self):
        self.update_window_size()
        self.state.handle_resize()
        self.update()
    
    def draw_fps(self):
        fps = str(int(self.clock.get_fps()))
        fps_t = self.font.render(fps , 1, pygame.Color("RED"), True)
        self.screen.blit(fps_t,(0,0))
    
    def update_window_size(self):
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
    
    def draw(self, screen):
        raise NotImplementedError
    
    def update(self):
        raise NotImplementedError

    def handle_resize(self):
        raise NotImplementedError
    
    def get_event(self, event):
        raise NotImplementedError

@cache
def scale_and_cache(image, target_size):
    return pygame.transform.scale(image, target_size)

@cache
def smoothscale_and_cache(image, target_size):
    return pygame.transform.smoothscale(image, target_size)

def load_all_gfx(directory, colorkey=(255, 0, 0), accept=(".svg", ".png", ".jpg")):
    graphics = {}

    for file in Path(directory).glob('**/*'):
        name, extension = file.stem, file.suffix

        if extension.lower() in accept:
            path = Path(directory / file)
            image = pygame.image.load(path)

            if extension.lower() == '.svg':
                low_quality_image = pygame.image.load_sized_svg(path, (200, 200))
                graphics[f'{name}_lq'] = low_quality_image

            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert((255, 0, 0))
                image.set_colorkey(colorkey)
                print('TOOLS.PY: CONVERTED IMAGE ALPHA')
            
            graphics[name] = image
        
    return graphics