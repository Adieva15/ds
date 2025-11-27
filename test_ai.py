import asyncio
import sys
import os

# Добавляем путь для импорта
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ai_coach import ai_fitness_coach
from config import AI_TOKEN, OPENAI_BASE_URL, OPENAI_MODEL


async def test_ai_directly():
    """Прямой тест ИИ без бота"""
    print("🔍 ТЕСТИРУЕМ ИИ...")
    print(f"📝 Модель: {OPENAI_MODEL}")
    print(f"🌐 URL: {OPENAI_BASE_URL}")
    print(f"🔑 Токен: {AI_TOKEN[:10]}..." if AI_TOKEN and len(AI_TOKEN) > 10 else "❌ Токен не настроен")

    test_messages = [
        "Привет! Как улучшить бег?",
        "Сколько нужно тренироваться в неделю?",
        "Устал от тренировок, что делать?"
    ]

    for i, message in enumerate(test_messages, 1):
        print(f"\n🧪 Тест {i}: '{message}'")
        try:
            response = await ai_fitness_coach(message)
            print(f"✅ Ответ ИИ: {response}")

            # Проверяем, не заготовленный ли ответ
            if any(word in response.lower() for word in ['ошибка', 'ключ', 'настройте', 'fallback']):
                print("❌ Похоже на заготовленный ответ!")
            else:
                print("🎉 Похоже на настоящий ИИ-ответ!")

        except Exception as e:
            print(f"❌ Ошибка: {e}")


if __name__ == "__main__":
    print("🚀 Запуск теста ИИ...")
    asyncio.run(test_ai_directly())