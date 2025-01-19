import pygame
from pathlib import Path
from data.utils.asset_helpers import gif_to_frames, pil_image_to_surface

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
                try:
                    image = image.convert((255, 0, 0))
                    image.set_colorkey(colorkey)
                    print('TOOLS.PY: CONVERTED IMAGE ALPHA')
                except Exception as error:
                    print('Invalid file:', name, extension)
                    raise error
            
            graphics[name] = image
        
    return graphics

def load_all_fonts(directory, accept=(".ttf")):
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

module_path = Path(__file__).parent
GRAPHICS = load_all_gfx((module_path / '../resources/graphics').resolve())
FONTS = load_all_fonts((module_path / '../resources/fonts').resolve())
SFX = load_all_sfx((module_path / '../resources/sfx').resolve())
MUSIC_PATHS = load_all_music((module_path / '../resources/music').resolve())