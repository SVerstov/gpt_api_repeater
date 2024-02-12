import asyncio
import logging

import lorem as lorem
from openai import AsyncOpenAI, APIError
from fastapi import HTTPException
from openai.types.chat import ChatCompletion
from pydantic import BaseModel
from starlette.requests import Request

from api.main import app
from config import Config
from utils.notifications import TgLogger

logger = logging.getLogger(__name__)


class GptSeoRequest(BaseModel):
    title: str
    description: str
    keys: list[str]


@app.post('/api/gpt_repeater')
async def gpt_repeater(request: Request, data: GptSeoRequest):
    config: Config = request.state.config

    tg_logger = TgLogger(config)
    await check_allow_ip(config, request)
    if data.title == '/test':
        await asyncio.sleep(5)
        return {'result': lorem.text()}
    try:

        openai_client = AsyncOpenAI(api_key=config.gpt.gpt_token)
        messages = await build_gpt_prompt(config, data)
        chat = await openai_client.chat.completions.create(
            model=config.gpt.model_name, messages=messages
        )
        reply = chat.choices[0].message.content
        logger.info(f'Успешная генерация Сео-описания для товара {data.title}')
        return {'result': reply}
    except APIError as e:
        msg = f'Ошибка генерации SEO-GPT APIError {e}'
        logger.error(msg, e, exc_info=True)
        await tg_logger.send_text(msg)
        raise HTTPException(status_code=500, detail="Ошибка генерации SEO-GPT APIError")
    except Exception as e:
        msg = f'Внезапная ошибка генерации SEO-GPT APIError {e}, {e.args=}'
        logger.error(msg, e, exc_info=True)
        await tg_logger.send_text(msg)
        raise HTTPException(status_code=500, detail="Ошибка генерации SEO-GPT APIError")


async def build_gpt_prompt(config, data):
    keys = list(filter(lambda x: len(x) > 2, data.keys))
    keys = "\n".join(keys)
    bot_msg = config.gpt.gpt_message.format(title=data.title, description=data.description, keys=keys)
    messages = [
        {"role": "user", "content": bot_msg},
    ]
    return messages


async def check_allow_ip(config, request):
    if request.client.host not in config.gpt.allowed_ips:
        logger.warning(f'Попытка доступа с несанкционированного ip {request.client.host}')
        raise HTTPException(status_code=403, detail="Access denied")
