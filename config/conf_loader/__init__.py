import logging
from dataclasses import dataclass

import yaml

from .main import MainConfig

logger = logging.getLogger(__name__)


@dataclass
class Config:
    main: MainConfig


def load_config() -> Config:
    with open("config/config.yaml", 'r', encoding='utf-8') as f:
        config_dct = yaml.safe_load(f)

    return Config(
        main=MainConfig.load_from_dict(config_dct["main"]),
    )
