import logging.config
from pathlib import Path

import yaml

logger = logging.getLogger(__name__)


def setup_logging():
    # Установка кодировки UTF-8 для журнала
    logger_conf_path = Path('config/logging.yaml')
    log_path = Path('log')
    try:
        log_path.mkdir(exist_ok=True)
        with logger_conf_path.open("r", encoding='utf-8') as f:
            logging_config = yaml.safe_load(f)
            logging.config.dictConfig(logging_config)
        logger.info("Logging configured successfully")
    except IOError:
        logging.basicConfig(level=logging.DEBUG)
        logger.warning("logging config file not found, use basic config")

