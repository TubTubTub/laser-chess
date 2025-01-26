import pygame
import threading
import sys
from pathlib import Path

from data.managers.window import window
from data.utils.load_helpers import load_gfx

FPS = 30
start_ticks = pygame.time.get_ticks()
logo_gfx_path = (Path(__file__).parent / '../resources/graphics/loading.png').resolve()

class LoadingScreen:
    def __init__(self, target_func):
        self._clock = pygame.time.Clock()
        self._thread = threading.Thread(target=target_func)
        self._thread.start()

        self._logo_surface = load_gfx(logo_gfx_path)
        self._logo_surface = pygame.transform.scale(self._logo_surface, (50, 50))
        self._logo_position = ((window.screen.size[0] - self._logo_surface.size[0]) / 2, (window.screen.size[1] - self._logo_surface.size[1]) / 2)

        self.run()
    
    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    
    def draw(self):
        window.screen.fill((0, 0, 0))

        opacity = min(255, (pygame.time.get_ticks() - start_ticks) / 5)
        self._logo_surface.set_alpha(opacity)
        window.screen.blit(self._logo_surface, self._logo_position)
        
        window.update()

    def run(self):
        while self._thread.is_alive():
            self.event_loop()
            self.draw()
            self._clock.tick(FPS)