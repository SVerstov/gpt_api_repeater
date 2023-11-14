import logging

import openai
from fastapi import HTTPException
from starlette.requests import Request

from api.main import app
from config import Config

logger = logging.getLogger(__name__)


@app.post('/api/gpt_repeater')
async def gpt_repeater(request: Request, title: str, keys: list[str]):
    config: Config = request.state.config
    if request.client.host != config.gpt.allowed_ip:
        raise HTTPException(status_code=403, detail="Access denied")

    keys = list(filter(lambda x: len(x) > 2, keys))
    keys = "\n".join(keys)
    bot_msg = config.gpt.gpt_message.format(title=title, keys=keys)
    messages = [
        {"role": "user", "content": bot_msg},
    ]
    openai.api_key = config.gpt.gpt_token
    chat = openai.ChatCompletion.create(
        model=config.gpt.model_name, messages=messages
    )
    reply = chat.choices[0].message.content
    return {'result': reply}
