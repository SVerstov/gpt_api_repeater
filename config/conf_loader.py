import logging
from dataclasses import dataclass
from typing import Self

import yaml

from config.messages import gpt_message

logger = logging.getLogger(__name__)


class ConfigBranch:
    """ Базовый класс для веток конфига с автоматической загрузкой параметров по аннотациям"""

    def __init__(self, dct: dict):
        for attr in self.__annotations__.keys():
            self.__setattr__(attr, dct.get(attr))
        self.after_load()
        for attr in self.__annotations__.keys():
            if self.__getattribute__(attr) is None and attr not in dct:
                logger.warning(f'Конфиг {self.__class__.__name__}: Отсутствует значение для параметра {attr}')

    def after_load(self):
        # Переопределить если нужны дополнительные действия с конфигом
        pass


class GPTConfig(ConfigBranch):
    gpt_token: str
    model_name: str
    gpt_message: str
    allowed_ip: str

    def after_load(self):
        pass
        self.gpt_message = gpt_message


@dataclass
class Config:
    gpt: GPTConfig

    def after_load(self):
        pass

    def __init__(self) -> Self:
        with open("config/config.yaml", 'r', encoding='utf-8') as f:
            config_dct = yaml.safe_load(f)

        for attr, config_branch in self.__annotations__.items():
            if issubclass(config_branch, ConfigBranch):
                self.__setattr__(attr, config_branch(config_dct[attr]))
        self.after_load()
