import pygame
from data.utils.settings_helpers import get_user_settings
user_settings = get_user_settings()

class AudioManager:
    def __init__(self, num_channels=16):
        pygame.mixer.set_num_channels(num_channels)

        self._music_volume = user_settings['musicVolume']
        self._sfx_volume = user_settings['sfxVolume']

        self._current_song = None
        self._current_channels = []
    
    def set_sfx_volume(self, volume):
        print('settings')
        self._sfx_volume = volume

        for channel in self._current_channels:
            channel.set_volume(self._sfx_volume)
    
    def set_music_volume(self, volume):
        self._music_volume = volume

        pygame.mixer.music.set_volume(self._music_volume)
    
    def pause_sfx(self):
        pygame.mixer.pause()
    
    def unpause_sfx(self):
        pygame.mixer.unpause(self)
    
    def prune_unused_channels(self):
        unused_channels = []
        for channel in self._current_channels:
            if channel.get_busy() is False:
                unused_channels.append(channel)

        return unused_channels
    
    def play_sfx(self, sfx):
        unused_channels = self.prune_unused_channels()
        
        if len(unused_channels) == 0:
            channel = pygame.mixer.find_channel()
        else:
            channel = unused_channels[0]

        if channel is None:
            print('No available channel for SFX (audio.py)')
            return
        
        self._current_channels.append(channel)
        channel.set_volume(self._sfx_volume)
        channel.play(sfx)
    
    def play_music(self, music_path):
        if music_path == self._current_song:
            return
        
        pygame.mixer.music.stop()
        pygame.mixer.music.unload()
        pygame.mixer.music.load(music_path)
        pygame.mixer.music.set_volume(self._music_volume)
        pygame.mixer.music.play(loops=-1)

        self._current_song = music_path

audio = AudioManager()