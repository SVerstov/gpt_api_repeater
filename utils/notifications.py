from logging import getLogger

from aiogram import Bot

from config import Config
from utils.singletone import SingletonMeta

logger = getLogger(__name__)


class TgLogger(metaclass=SingletonMeta):
    prefix = "GPT_SERVER:"

    def __init__(self, config: Config):
        self.bot = Bot(token=config.bot.token)
        self.log_chat = config.bot.log_chat

    async def send_text(self, msg: str):
        try:
            msg = f"{self.prefix} {msg}"
            await self.bot.send_message(self.log_chat, msg, parse_mode=None)
        except Exception as e:
            logger.error(
                f"Ошибка отправки сообщения в логчат {e} {e.args=}",
                exc_info=True,
            )
