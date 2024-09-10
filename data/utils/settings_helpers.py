import json
from pathlib import Path

module_path = Path(__file__).parent

def get_settings_json():
    file_path = (module_path / 'app_data/app_settings.json').resolve()
    with open(file_path) as f:
        file = json.load(f)

    return file