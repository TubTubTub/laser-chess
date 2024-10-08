import json
from pathlib import Path

module_path = Path(__file__).parent
default_file_path = (module_path / '../app_data/default_settings.json').resolve()
user_file_path = (module_path / '../app_data/user_settings.json').resolve()

def get_user_settings():
    try:
        with open(user_file_path, 'r') as f:
            file = json.load(f)

        return file
    except:
        raise Exception('Invalid JSON file (settings_helpers.py)')

def update_user_settings(data):
    try:
        with open(user_file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        raise Exception('Invalid JSON file (settings_helpers.py)')

def get_default_settings():
    try:
        with open(default_file_path, 'r') as f:
            file = json.load(f)
        
        return file
    except:
        raise Exception('Invalid JSON file (settings_helpers.py)')