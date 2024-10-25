import pygame
from PIL import Image
from pygame._sdl2 import Window
from pathlib import Path
from functools import cache
from data.constants import BackgroundType

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

        self.state.update(current_time=current_time, delta_time=delta_time)
        
        self.draw_fps()
        pygame.display.update()

    def main_game_loop(self):
        while not self.done:
            self.event_loop()
            self.update()
    
    def resize_window(self):
        self.update_native_window_size()
        self.state.handle_resize()
        self.update()
    
    # def draw_background(self):
        
    
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

@cache
def scale_and_cache(image, target_size):
    return pygame.transform.scale(image, target_size)

@cache
def smoothscale_and_cache(image, target_size):
    return pygame.transform.smoothscale(image, target_size)

def gif_to_frames(path):
    try:
        image = Image.open(path)

        first_frame = image.copy().convert('RGBA')
        yield first_frame
        image.seek(1)

        while True:
            current_frame = image.copy()
            yield current_frame
            image.seek(image.tell() + 1)
    except EOFError:
        pass

def pil_image_to_surface(pil_image):
    return pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode).convert()

def load_all_gfx(directory, colorkey=(255, 0, 0), accept=(".svg", ".png", ".jpg", ".gif")):
    graphics = {}

    for file in Path(directory).rglob('*'):
        name, extension = file.stem, file.suffix
        path = Path(directory / file)

        if extension.lower() in accept:
            if extension.lower() == '.gif':
                frames_list = []

                for frame in gif_to_frames(path):
                    image_surface = pil_image_to_surface(frame)
                    frames_list.append(image_surface)

                graphics[name] = frames_list
                continue

            elif extension.lower() == '.svg':
                low_quality_image = pygame.image.load_sized_svg(path, (200, 200))
                graphics[f'{name}_lq'] = low_quality_image

            image = pygame.image.load(path)

            if image.get_alpha():
                image = image.convert_alpha()
            else:
                image = image.convert((255, 0, 0))
                image.set_colorkey(colorkey)
                print('TOOLS.PY: CONVERTED IMAGE ALPHA')
            
            graphics[name] = image
        
    return graphics

module_path = Path(__file__).parent
GRAPHICS = load_all_gfx((module_path / '../resources/graphics').resolve())

def calculate_frame_index(elapsed_milliseconds, start_index, end_index, fps):
    ms_per_frame = int(1000 / fps)
    return start_index + ((elapsed_milliseconds // ms_per_frame) % (end_index - start_index))

def draw_background(screen, current_time, background_type):
    match background_type:
        case BackgroundType.DEFAULT:
            frame_index = calculate_frame_index(current_time, 0, len(GRAPHICS['background']), fps=8)
            scaled_background = scale_and_cache(GRAPHICS['background'][frame_index], screen.size)
            screen.blit(scaled_background, (0, 0))
        case BackgroundType.GAME:
            pass

        case _:
            raise ValueError('Unhandled background type! (draw_background)')