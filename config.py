# === НАСТРОЙКИ ===
import os

BOT_TOKEN='7353196699:AAG8KiNUIgeuQe1JwYsc5P1FOFYoS1JSHSA'
AI_TOKEN='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'

# Настройки OpenAI
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"

OPENAI_MODEL = "qwen/qwen3-embedding-8b"

DATABASE_URL='sqlite:///fitness_bot.db'

# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

