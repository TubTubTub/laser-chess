from data.utils.data_helpers import get_themes, get_user_settings

THEMES = get_themes()
user_settings = get_user_settings()

def flatten_dictionary_generator(dictionary, parent_key):
    for key, value in dictionary.items():
        if parent_key:
            new_key = parent_key + key.capitalize()
        else:
            new_key = key

        if isinstance(value, dict):
            yield from flatten_dictionary(value, new_key).items()
        else:
            yield new_key, value

def flatten_dictionary(dictionary, parent_key=''):
    return dict(flatten_dictionary_generator(dictionary, parent_key))

def recursive_lookup(key, dictionary):
    if key in dictionary:
        return dictionary[key]

    for nested_dictionary in dictionary.values():
        if isinstance(nested_dictionary, dict):
            return recursive_lookup(key, nested_dictionary)

class ThemeManager:
    def __init__(self, colour_mode="light"):
        self._colour_mode = colour_mode

        self.__dict__.update(flatten_dictionary(THEMES['colours'][colour_mode]))
        self.__dict__.update(THEMES['dimensions'])
    
    def __getitem__(self, arg):
        item = self.__dict__.get(arg)
        
        if item is None:
            raise KeyError('(ThemeManager.__getitem__) Requested theme item not found:', arg)
        
        return item
    
    # def get_colour(self, key):
    #     result = recursive_lookup(key,s self._colours)

    #     if result is None:
    #         raise ValueError(f'(Theme.get_colour) Key "{key}" not found in theme colours!')

    #     return result
    
    # def get_dimension(self, key):
    #     result = recursive_lookup(key, self._dimensions)

    #     if result is None:
    #         raise ValueError(f'(Theme.get_dimension) Key "{key}" not found in theme dimensions!')

    #     return result
    
    def set_colour_mode(self, colour_mode):
        if colour_mode:
            self._colour_mode = 'dark'
        else:
            self._colour_mode = 'light'

theme = ThemeManager(user_settings['colourMode'])