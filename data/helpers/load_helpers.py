import pygame
import pygame.freetype
from pathlib import Path
from data.helpers.asset_helpers import gif_to_frames, pil_image_to_surface

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

        if extension.lower() in accept and 'old' not in name:
            if name == 'piece_spritesheet':
                data = load_spritesheet(
                    path,
                    (16, 16),
                    ['pyramid_1', 'scarab_1', 'anubis_1', 'pharaoh_1', 'sphinx_1', 'pyramid_0', 'scarab_0', 'anubis_0', 'pharaoh_0', 'sphinx_0'],
                    ['_a', '_b', '_c', '_d'])

                graphics = graphics | data
                continue

            data = load_gfx(path, colorkey, accept)

            if isinstance(data, list):
                graphics[name] = data[0]
                graphics[f'{name}_lq'] = data[1]
            else:
                graphics[name] = data

    return graphics

def load_spritesheet(path, sprite_size, col_names, row_names):
    spritesheet = load_gfx(path)
    col_count = int(spritesheet.width / sprite_size[0])
    row_count = int(spritesheet.height / sprite_size[1])

    sprite_dict = {}

    for column in range(col_count):
        for row in range(row_count):
            surface = pygame.Surface(sprite_size, pygame.SRCALPHA)
            name = col_names[column] + row_names[row]

            surface.blit(spritesheet, (0, 0), (column * sprite_size[0], row * sprite_size[1], *sprite_size))
            sprite_dict[name] = surface

    return sprite_dict

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

        if extension.lower() in accept and 'old' not in name:
            sound_effects[name] = load_sfx(path)

    return sound_effects

def load_sfx(path, accept=(".mp3", ".wav", ".ogg")):
    file_path = Path(path)
    name, extension = file_path.stem, file_path.suffix

    if extension.lower() in accept:
        sfx = pygame.mixer.Sound(path)
        return sfx

def load_all_music(directory, accept=(".mp3", ".wav", ".ogg")):
    music_paths = {}
    for file in Path(directory).rglob('*'):
        name, extension = file.stem, file.suffix
        path = Path(directory / file)

        if extension.lower() in accept:
            music_paths[name] = path

    return music_paths