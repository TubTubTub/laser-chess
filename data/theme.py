from data.utils.data_helpers import get_themes, get_user_settings

THEMES = get_themes()
print(THEMES)
user_settings = get_user_settings()

def recursive_lookup(key, dictionary):
    print(key, dictionary)
    if key in dictionary:
        return dictionary[key]

    for nested_dictionary in dictionary.values():
        if isinstance(nested_dictionary, dict):
            return recursive_lookup(key, nested_dictionary)

class Theme:
    def __init__(self, colour_mode="light"):
        self._colour_mode = colour_mode
        self._colours = THEMES['colours'][colour_mode]
        self._dimensions = THEMES['dimensions']
    
    def get_colour(self, key):
        result = recursive_lookup(key, self._colours)

        if result is None:
            raise ValueError(f'(Theme.get_colour) Key "{key}" not found in theme colours!')

        return result
    
    def get_dimension(self, key):
        result = recursive_lookup(key, self._dimensions)

        if result is None:
            raise ValueError(f'(Theme.get_dimension) Key "{key}" not found in theme dimensions!')

        return result
    
    def set_colour_mode(self, colour_mode):
        if colour_mode:
            self._colour_mode = 'dark'
        else:
            self._colour_mode = 'light'

theme = Theme(user_settings['colourMode'])