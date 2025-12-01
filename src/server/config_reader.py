from pathlib import Path


from typing import AsyncGenerator
from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from tortoise import Tortoise


from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

#наследует до папочки src
ROOT_DIR = Path(__file__).parent.parent

class Config(BaseSettings):
    BOT_TOKEN: SecretStr
    DB_URL:SecretStr

    #ccылка на бэкенд
    # WEBHOOK_URL: str ="https://qdsnn-85-192-49-179.a.free.pinggy.link"
    WEBHOOK_URL: str ="https://salty-snakes-move.loca.lt"

    # ссылка на фронтенд
    # WEBAPP_URL: str="https://palladic-cheree-noncommendably.ngrok-free.dev"
    WEBAPP_URL: str="https://spovatar-miniapp.loca.lt"
    #на каком хосту и порту работает fastapi
    APP_HOST:str="localhost"
    APP_PORT:int = 8080

    #полный путь к dotenv
    model_config =  SettingsConfigDict(
        env_file = ROOT_DIR/"server"/".env",
        env_file_encoding = "utf-8"
    )
    
config = Config()


TORTOISE_ORM = {
    "connections": {"default": config.DB_URL.get_secret_value()},
    "apps": {
        "models": {
            "models": ["db.models.user", "aerich.models"],
            "default_connection": "default",
        },
    },
}
async def lifespan(app: FastAPI) -> AsyncGenerator:
    try:
        await bot.set_webhook(
            url=f"{config.WEBHOOK_URL}/webhook",
            allowed_updates = dp.resolve_used_update_types(),
            drop_pending_updates=True
        )
        print('webhook успешно установлен')
    except Exception as e:
        print(f'не удалось установить webhook: {e}')
    await Tortoise.init(TORTOISE_ORM)
    yield
    await Tortoise.close_connections()
    await bot.session.close()


bot = Bot(config.BOT_TOKEN.get_secret_value())
dp = Dispatcher()

#lifespan - для стартапа
app = FastAPI(lifespan=lifespan)

