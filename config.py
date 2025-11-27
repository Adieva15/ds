# === НАСТРОЙКИ ===
import os

BOT_TOKEN=''
AI_TOKEN=''

# Настройки OpenAI
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"

OPENAI_MODEL = "x-ai/grok-4.1-fast:free"

DATABASE_URL='sqlite:///fitness_bot.db'

# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

