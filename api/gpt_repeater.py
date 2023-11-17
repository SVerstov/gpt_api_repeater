import asyncio
import logging

import lorem as lorem
from openai import AsyncOpenAI
from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from api.main import app
from config import Config

logger = logging.getLogger(__name__)


class GptSeoRequest(BaseModel):
    title: str
    description: str
    keys: list[str]


@app.post('/api/gpt_repeater')
async def gpt_repeater(request: Request, data: GptSeoRequest):
    config: Config = request.state.config
    if request.client.host not in config.gpt.allowed_ips:
        raise HTTPException(status_code=403, detail="Access denied")
    if data.title == '/test':
        await asyncio.sleep(5)
        return {'result': lorem.text()}

    openai_client = AsyncOpenAI(api_key=config.gpt.gpt_token)
    keys = list(filter(lambda x: len(x) > 2, data.keys))
    keys = "\n".join(keys)
    bot_msg = config.gpt.gpt_message.format(title=data.title, description=data.description,keys=keys)
    messages = [
        {"role": "user", "content": bot_msg},
    ]
    chat = await openai_client.chat.completions.create(
        model=config.gpt.model_name, messages=messages
    )
    reply = chat.choices[0].message.content
    return {'result': reply}
