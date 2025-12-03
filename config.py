
import os

BOT_TOKEN='7353196699:AAF7A1bm48TRHvFXN7ZznUfSKUr6_aJM-cE'

GIGACHAT_TOKEN = "MDE5YWJjODEtNmNhOC03NjI4LTg5YWMtMzJiZjMxNjA2NDcyOjQ0MDY1ZGFiLThiNjktNDQwZi05MGE0LTkwODViMWFmOGVkYw=="  # Полученный токен или путь к файлу с токеном
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"  # Область доступа
GIGACHAT_MODEL = "GigaChat-2-Max"

DATABASE_URL='sqlite:///fitness_bot.db'

WEB_APP_URL = 'https://Adievadine.pythonanywhere.com'
# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO,
format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                    )
logger = logging.getLogger(__name__)

