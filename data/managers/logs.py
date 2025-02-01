import logging.config
from data.utils.data_helpers import load_json
from pathlib import Path
import logging

config_path = (Path(__file__).parent / '../app_data/logs_config.json').resolve()

class LogsManager:
    def __init__(self):
        config = load_json(config_path)
        logging.config.dictConfig(config)

logger = LogsManager()