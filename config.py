
import os

BOT_TOKEN=''
AI_TOKEN=''

# Настройки OpenAI
# OPENAI_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

# OPENAI_MODEL = "prime-intellect/intellect-3"
GIGACHAT_TOKEN = "MDE5YWJjODEtNmNhOC03NjI4LTg5YWMtMzJiZjMxNjA2NDcyOmVkOWVjMDY3LTRiNzEtNDM0ZS1iM2M4LTg4YTQxOTY2MTk0Zg=="  # Полученный токен или путь к файлу с токеном
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"  # Область доступа
GIGACHAT_MODEL = "GigaChat-2-Max"

DATABASE_URL='sqlite:///fitness_bot.db'

WEB_APP_URL = 'https://Adievadine.pythonanywhere.com'
# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

