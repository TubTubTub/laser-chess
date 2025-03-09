import pygame
from data.helpers.asset_helpers import scale_and_cache

FPS = 60

class AnimationManager:
    def __init__(self):
        self._current_ms = 0
        self._timers = []

    def set_delta_time(self):
        self._current_ms = pygame.time.get_ticks()

        for timer in self._timers:
            start_ms, target_ms, callback = timer
            if self._current_ms - start_ms >= target_ms:
                callback()
                self._timers.remove(timer)

    def calculate_frame_index(self, start_index, end_index, fps):
        ms_per_frame = int(1000 / fps)
        return start_index + ((self._current_ms // ms_per_frame) % (end_index - start_index))

    def draw_animation(self, screen, animation, position, size, fps=8):
        frame_index = self.calculate_frame_index(0, len(animation), fps)
        scaled_animation = scale_and_cache(animation[frame_index], size)
        screen.blit(scaled_animation, position)

    def draw_image(self, screen, image, position, size):
        scaled_background = scale_and_cache(image, size)
        screen.blit(scaled_background, position)

    def set_timer(self, target_ms, callback):
        self._timers.append((self._current_ms, target_ms, callback))

animation = AnimationManager()