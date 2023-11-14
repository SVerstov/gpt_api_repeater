import logging

import openai
from fastapi import HTTPException
from pydantic import BaseModel
from starlette.requests import Request

from api.main import app
from config import Config

logger = logging.getLogger(__name__)


class GptSeoRequest(BaseModel):
    title: str
    keys: list[str]


@app.post('/api/gpt_repeater')
async def gpt_repeater(request: Request, data: GptSeoRequest):
    config: Config = request.state.config
    if request.client.host not in config.gpt.allowed_ips:
        raise HTTPException(status_code=403, detail="Access denied")

    keys = list(filter(lambda x: len(x) > 2, data.keys))
    keys = "\n".join(keys)
    bot_msg = config.gpt.gpt_message.format(title=data.title, keys=keys)
    messages = [
        {"role": "user", "content": bot_msg},
    ]
    openai.api_key = config.gpt.gpt_token
    chat = openai.ChatCompletion.create(
        model=config.gpt.model_name, messages=messages
    )
    reply = chat.choices[0].message.content
    return {'result': reply}
