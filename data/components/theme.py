from data.utils.data_helpers import get_themes

THEMES = get_themes()

class Theme:
    def __init__(self, colour_mode="light"):
        self._colour_mode = colour_mode
        self.colours = THEMES['colours'][colour_mode]
        self.dimensions = THEMES['dimensions']
    
    def get_colour(self, key):
        if key in self.colours:
            return self.colours[key]

        for key, value in self.colours.items():
            if isinstance(value, dict):
                result = self.get_colour(key, value)

                if result:
                    return result
    
    def get_dimension(self, key):
        if key in self.dimensions:
            return self.dimensions[key]

        for key, value in self.dimensions.items():
            if isinstance(value, dict):
                result = self.get_colour(key, value)

                if result:
                    return result
    
    def set_colour_mode(self, colour_mode):
        if colour_mode:
            self._colour_mode = 'dark'
        else:
            self._colour_mode = 'light'