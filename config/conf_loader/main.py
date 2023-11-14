from dataclasses import dataclass
from typing import Self


@dataclass
class MainConfig:
    gpt_token: str
    model_name: str

    @classmethod
    def load_from_dict(cls, dct: dict) -> Self:
        conf_dict = {}
        for attr in cls.__annotations__.keys():
            conf_dict[attr] = dct.get(attr)
        return cls(**conf_dict)




