from pathlib import Path
from data.utils.load_helpers import *

module_path = Path(__file__).parent
GRAPHICS = load_all_gfx((module_path / '../resources/graphics').resolve())
FONTS = load_all_fonts((module_path / '../resources/fonts').resolve())
SFX = load_all_sfx((module_path / '../resources/sfx').resolve())
MUSIC_PATHS = load_all_music((module_path / '../resources/music').resolve())