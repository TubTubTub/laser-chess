import pygame
from data.helpers.data_helpers import get_user_settings
from data.managers.logs import initialise_logger

logger = initialise_logger(__name__)
user_settings = get_user_settings()

class AudioManager:
    def __init__(self, num_channels=16):
        pygame.mixer.set_num_channels(num_channels)

        self._music_volume = user_settings['musicVolume']
        self._sfx_volume = user_settings['sfxVolume']

        self._current_song = None
        self._current_channels = []

    def set_sfx_volume(self, volume):
        self._sfx_volume = volume

        for channel in self._current_channels:
            channel.set_volume(self._sfx_volume)

    def set_music_volume(self, volume):
        self._music_volume = volume

        pygame.mixer.music.set_volume(self._music_volume)

    def pause_sfx(self):
        pygame.mixer.pause()

    def unpause_sfx(self):
        pygame.mixer.unpause()

    def stop_sfx(self, fadeout=0):
        pygame.mixer.fadeout(fadeout)

    def remove_unused_channels(self):
        unused_channels = []
        for channel in self._current_channels:
            if channel.get_busy() is False:
                unused_channels.append(channel)

        return unused_channels

    def play_sfx(self, sfx, loop=False):
        unused_channels = self.remove_unused_channels()

        if len(unused_channels) == 0:
            channel = pygame.mixer.find_channel()
        else:
            channel = unused_channels.pop(0)

        if channel is None:
            logger.warning('No available channel for SFX')
            return

        self._current_channels.append(channel)
        channel.set_volume(self._sfx_volume)

        if loop:
            channel.play(sfx, loops=-1)
        else:
            channel.play(sfx)

    def play_music(self, music_path):
        if 'menu' in str(music_path) and 'menu' in str(self._current_song):
            return

        if music_path == self._current_song:
            return

        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self._music_volume)
        pygame.mixer.music.play(loops=-1)

        self._current_song = music_path

audio = AudioManager()