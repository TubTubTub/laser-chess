import pygame
from pathlib import Path

import pygame.freetype
from data.utils.asset_helpers import gif_to_frames, pil_image_to_surface

def convert_gfx_alpha(image, colorkey=(0, 0, 0)):
    # if image.get_alpha():
        return image.convert_alpha()
    # else:
    #     image = image.convert_alpha()
    #     image.set_colorkey(colorkey)

    #     return image

def load_gfx(path, colorkey=(0, 0, 0), accept=(".svg", ".png", ".jpg", ".gif")):
    file_path = Path(path)
    name, extension = file_path.stem, file_path.suffix

    if extension.lower() in accept:
        if extension.lower() == '.gif':
            frames_list = []

            for frame in gif_to_frames(path):
                image_surface = pil_image_to_surface(frame)
                frames_list.append(image_surface)
            
            return frames_list

        if extension.lower() == '.svg':
            low_quality_image = pygame.image.load_sized_svg(path, (200, 200))
            image = pygame.image.load(path)
            image = convert_gfx_alpha(image, colorkey)

            return [image, low_quality_image]

        else:
            image = pygame.image.load(path)
            return convert_gfx_alpha(image, colorkey)

def load_all_gfx(directory, colorkey=(0, 0, 0), accept=(".svg", ".png", ".jpg", ".gif")):
    graphics = {}

    for file in Path(directory).rglob('*'):
        name, extension = file.stem, file.suffix
        path = Path(directory / file)

        if extension.lower() in accept:
            data = load_gfx(path, colorkey, accept)

            if isinstance(data, list):
                graphics[name] = data[0]
                graphics[f'{name}_lq'] = data[1]
            else:
                graphics[name] = data
        
    return graphics

def load_all_fonts(directory, accept=(".ttf", ".otf")):
    fonts = {}
    
    for file in Path(directory).rglob('*'):
        name, extension = file.stem, file.suffix
        path = Path(directory / file)

        if extension.lower() in accept:
            font = pygame.freetype.Font(path)
            fonts[name] = font
    
    return fonts

def load_all_sfx(directory, accept=(".mp3", ".wav", ".ogg")):
    sound_effects = {}

    for file in Path(directory).rglob('*'):
        name, extension = file.stem, file.suffix
        path = Path(directory / file)

        if extension.lower() in accept:
            sfx = pygame.mixer.Sound(path)
            sound_effects[name]= sfx
    
    return sound_effects

def load_all_music(directory, accept=(".mp3", ".wav", ".ogg")):
    music_paths = {}
    for file in Path(directory).rglob('*'):
        name, extension = file.stem, file.suffix
        path = Path(directory / file)

        if extension.lower() in accept:
            music_paths[name] = path
    
    return music_paths