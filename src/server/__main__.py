#корректные проходу запросов бэкенда и фронтенда
from fastapi.middleware.cors import CORSMiddleware

#для запуска приложения отсюда
import uvicorn
from bot.handlers import setup_routers as setup_bot_routers
from api import setup_routers as setup_api_routers

from config_reader import dp, config, app


#для продакшна указать какие штучки доступные
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# подключение роутеров бота и апи
dp.include_router(setup_bot_routers())

app.include_router(setup_api_routers())

if __name__=="__main__":
    uvicorn.run(app, host=config.APP_HOST, port=config.APP_PORT)