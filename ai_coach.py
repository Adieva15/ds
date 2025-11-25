from openai import OpenAI
from config import AI_TOKEN, OPENAI_BASE_URL, OPENAI_MODEL
from user_data import get_user_data  # ⬅ Импортируем из user_data.py
import random

async def ai_fitness_coach(user_message, user_id=None):
    client = OpenAI(base_url=OPENAI_BASE_URL, api_key=AI_TOKEN)

    # Получаем контекст пользователя
    user_context = get_user_data(user_id)
    workouts_count = user_context["workouts"]
    goals = user_context["goals"]

    prompt = f"""
    Ты - виртуальный фитнес-тренер Spovatar! Отвечай кратко (1-2 предложения), эмоционально, с эмодзи.

    КОНТЕКСТ ПОЛЬЗОВАТЕЛЯ:
    - Тренировок всего: {workouts_count}
    - Цели: {goals}

    СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЯ: "{user_message}"

    ТВОИ ВОЗМОЖНОСТИ:
    🏋️ Анализировать тренировки
    💬 Давать персональные советы  
    🎯 Помогать с целями
    🌟 Мотивировать
    📊 Оценивать прогресс

    ОТВЕЧАЙ КАК ДРУГ-ТРЕНЕР! Будь конкретным и полезным.
    """

    try:
        response = client.chat.completions.create(
            model=OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8
        )
        return response.choices[0].message.content
    except Exception as e:
        # Запасные ответы
        fallback_responses = [
            "Отлично поработал! 💪 Продолжай в том же духе!",
            "Ты на правильном пути! 🚀 Горжусь твоим прогрессом!",
            "Каждая тренировка делает тебя сильнее! 🔥 Не сдавайся!",
            "Ты молодец! 🌟 Завтра будет еще лучше!",
            "Супер! Помни: регулярность - ключ к успеху! 🗝️"
        ]
        return random.choice(fallback_responses)