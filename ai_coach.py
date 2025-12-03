
from langchain_gigachat.chat_models import GigaChat
from langchain_core.messages import HumanMessage
from config import GIGACHAT_TOKEN, GIGACHAT_SCOPE, GIGACHAT_MODEL, logger
from user_data import get_user_data
import random
import asyncio


class GigaChatClient:
    def __init__(self):
        self.client = GigaChat(
            model=GIGACHAT_MODEL or "GigaChat-2-Max",
            credentials=GIGACHAT_TOKEN,
            scope=GIGACHAT_SCOPE or "GIGACHAT_API_PERS",
            verify_ssl_certs=False,
            temperature=0.7,
            profanity_check=False,
            max_tokens=500
        )
        logger.info("GigaChat client initialized")

    async def invoke_async(self, prompt):
        """Асинхронный вызов GigaChat"""
        try:
            messages = [HumanMessage(content=prompt)]
            response = await asyncio.to_thread(self.client.invoke, messages)
            return response.content
        except Exception as e:
            logger.error(f"Ошибка при вызове GigaChat: {e}")
            return None


# Создаем глобальный экземпляр клиента
giga_client = GigaChatClient()


async def ai_fitness_coach(user_message, user_id=None, function_type=None):
    """Основная функция для взаимодействия с GigaChat"""
    user_context = get_user_data(user_id)
    workouts_count = user_context.get('workouts', 0)
    goals = user_context.get('goals', ['стать сильнее'])

    if function_type is None:
        function_type = detect_function_type(user_message)
    
    function_instructions = {
        "analyze": "Проанализируй тренировки пользователя. Задай вопросы о тренировках или проанализируй прогресс. Не хвали просто так.",
        "advice": "Дай персональный совет. Спроси о проблемах и дай конкретные рекомендации. Не хвали без причины.",
        "goals": "Помоги поставить цель. Задай уточняющие вопросы о желаемой цели. Не хвали в ответ на запрос о целях.",
        "motivate": "Мотивируй пользователя. Вдохновляй и поддерживай. Хвали уместно.",
        "progress": "Оцени прогресс пользователя. Дай объективную оценку достижений. Не хвали без анализа."
    }

    instruction = function_instructions.get(function_type, "Ответь на запрос пользователя")

    prompt = f"""{instruction}

Контекст: {workouts_count} тренировок, цели: {goals}
Сообщение пользователя: "{user_message}"

Отвечай кратко (1-2 предложения), с эмодзи. Будь конкретным и полезным.
Не отвечай общими фразами! Не хвали без причины!
Твой ответ (только ответ, без пояснений):"""

    try:
        response = await giga_client.invoke_async(prompt)
        
        if response and response.strip():
            # Убираем возможные лишние кавычки или форматирование
            response = response.strip().strip('"').strip()
            return response
        else:
            logger.error("Пустой ответ от GigaChat")
            return get_fallback_response(function_type)
            
    except Exception as e:
        logger.error(f"Ошибка AI: {e}")
        return get_fallback_response(function_type)


def detect_function_type(message):
    """Автоматически определяет тип функции по тексту сообщения"""
    message_lower = message.lower()

    if any(word in message_lower for word in ['анализ', 'разбор', 'проанализир', 'оцени тренировк']):
        return "analyze"
    elif any(word in message_lower for word in
             ['совет', 'рекомендац', 'как улучшить', 'как сделать', 'помоги', 'что делать']):
        return "advice"
    elif any(word in message_lower for word in ['цель', 'хочу достичь', 'поставить цель', 'планир']):
        return "goals"
    elif any(word in message_lower for word in ['мотивац', 'устал', 'нет сил', 'лень', 'хочется бросить']):
        return "motivate"
    elif any(word in message_lower for word in ['прогресс', 'улучшен', 'результат', 'достижен']):
        return "progress"
    else:
        return "advice"


def get_fallback_response(function_type=None):
    """Запасные ответы при ошибках API"""
    fallback_responses = {
        "analyze": [
            "Расскажи о своих последних тренировках? 🏋️ Какие упражнения делал?",
            "Давай разберем твои тренировки! Что получается лучше всего?"
        ],
        "advice": [
            "С какими сложностями сталкиваешься? Помогу найти решение! 💪",
            "Что именно хочешь улучшить в тренировках?"
        ],
        "goals": [
            "Какую цель хочешь поставить? 🎯 Расскажи подробнее!",
            "Давай поставим конкретную цель! Что для тебя важно сейчас?"
        ],
        "motivate": [
            "Ты делаешь крутые успехи! Продолжай в том же духе! 🚀",
            "Каждая тренировка приближает к цели! Ты молодец! 🔥"
        ],
        "progress": [
            "Расскажи о своих успехах! 📊 Что изменилось за последнее время?",
            "Заметил ли ты улучшения в силе или выносливости? 💪"
        ]
    }

    if function_type and function_type in fallback_responses:
        return random.choice(fallback_responses[function_type])
    else:
        return random.choice([
            "Расскажи больше о своей ситуации! 🤔",
            "Что именно тебя интересует? Помогу разобраться! 💪"
        ])


# Пример синхронного использования (для тестов)
def test_sync():
    """Тестовая синхронная функция для проверки работы"""
    test_prompt = "Привет, помоги мне составить план тренировок"
    
    try:
        messages = [HumanMessage(content=test_prompt)]
        response = giga_client.client.invoke(messages)
        print(f"Ответ GigaChat: {response.content}")
        return response.content
    except Exception as e:
        print(f"Ошибка: {e}")
        return None