
import os

BOT_TOKEN='7353196699:AAG8KiNUIgeuQe1JwYsc5P1FOFYoS1JSHSA'
AI_TOKEN='sk-or-v1-f3ccfb91fd625346fc1c0765584185a7201555ab4a5d0117b4deaa24de86978bS'

# Настройки OpenAI
OPENAI_BASE_URL = "https://openrouter.ai/api/v1/chat/completions"

OPENAI_MODEL = "prime-intellect/intellect-3"

DATABASE_URL='sqlite:///fitness_bot.db'

WEB_APP_URL = 'https://Adievadine.pythonanywhere.com'
# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

