
import os

BOT_TOKEN=''

GIGACHAT_TOKEN = ""  # Полученный токен или путь к файлу с токеном
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

