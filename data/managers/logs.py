import logging.config
from data.helpers.data_helpers import load_json
from pathlib import Path
import logging

config_path = (Path(__file__).parent / '../app_data/logs_config.json').resolve()
config = load_json(config_path)
logging.config.dictConfig(config)

def initialise_logger(file_path):
    return logging.getLogger(Path(file_path).name)