# === НАСТРОЙКИ ===
import os
import logging
import base64


BOT_TOKEN = '7353196699:AAG8KiNUIgeuQe1JwYsc5P1FOFYoS1JSHSA'

# Настройки OpenAI
# OPENAI_BASE_URL = "https://openrouter.ai/api/v1"
OPENAI_BASE_URL="https://ngw.devices.sberbank.ru:9443/api/v1/"
OPENAI_MODEL ='GigaChat-2-lite'

# Настройки логирования
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


client_id = "019abc81-6ca8-7628-89ac-32bf31606472"
client_secret = "7efab00d-2d84-4d16-ab0d-7a36ce9df3e0"

# Создаем строку для кодирования
credentials = f"{client_id}:{client_secret}"

AI_TOKEN = base64.b64encode(credentials.encode()).decode()

# print(f"Ваш AI_TOKEN: {AI_TOKEN}")