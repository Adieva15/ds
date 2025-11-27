# === НАСТРОЙКИ ===
import os

BOT_TOKEN='7353196699:AAG8KiNUIgeuQe1JwYsc5P1FOFYoS1JSHSA'


# === OLLAMA ===
AI_TOKEN='24cde5322ac74f469cf1e2de3f3ec963.ZpmIu5U38dnJxyBuj0fPRVTS'

# Настройки OpenAI
OPENAI_BASE_URL = "https://ollama.com"

OPENAI_MODEL = "qwen3vl"

DATABASE_URL='sqlite:///fitness_bot.db'

# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

