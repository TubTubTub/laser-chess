import json
from pathlib import Path

module_path = Path(__file__).parent

class Settings:
    def __init__(self, file_location):
        dictionary = self.load_settings_json(file_location)
        self.__dict__.update(dictionary)
    
    def load_settings_json(self, location):
        with open(location) as f:
            file = json.load(f)

        return file

app_settings = Settings((module_path / 'app_data/app_settings.json').resolve())