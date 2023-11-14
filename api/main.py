import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from uvicorn import run

from config import Config

logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_config_middleware(request: Request, call_next):
    """ Добавляет config в request,
     Доставать так:
      config: Config = request.state.config
    """
    request.state.config = Config()
    return await call_next(request)


def run_fastapi():
    run(app, host="0.0.0.0", port=5000)
