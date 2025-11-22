# === НАСТРОЙКИ ===
import os

# Токены
AI_TOKEN = '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'
BOT_TOKEN = '7971545933:AAHJpI7CzpfvlYVF5y9liUqx4RyjDMJbmPA'

# Настройки OpenAI
OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_MODEL = "x-ai/grok-4.1-fast:free"

# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

