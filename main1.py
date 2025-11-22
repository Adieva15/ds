import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI

# === НАСТРОЙКИ ===
ai_token = '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'
bot_token = '7971545933:AAHJpI7CzpfvlYVF5y9liUqx4RyjDMJbmPA'

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === ПРОСТАЯ ПАМЯТЬ ===
user_data = {}  # Храним в оперативке: {user_id: {"workouts": 5, "last_workout": "утро"}}


# === КЛАВИАТУРЫ ===
def main_keyboard():
    buttons = [
        ['🏋️ Записал тренировку', '📊 Мой прогресс'],
        ['💬 Совет тренера', '🌟 Мотивация'],
        ['🎯 Поставить цель', '🆘 Помощь']
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


# === УМНЫЙ ИИ-ТРЕНЕР ===
async def ai_fitness_coach(user_message, user_id=None):
    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=ai_token)

    # Получаем контекст пользователя
    user_context = user_data.get(user_id, {"workouts": 0, "goals": []})

    prompt = f"""
    Ты - виртуальный фитнес-тренер Spovatar. Отвечай кратко (1-2 предложения), эмоционально, с эмодзи.

    КОНТЕКСТ ПОЛЬЗОВАТЕЛЯ:
    - Тренировок всего: {user_context['workouts']}
    - Цели: {user_context.get('goals', ['стать сильнее'])}

    СООБЩЕНИЕ ПОЛЬЗОВАТЕЛЯ: "{user_message}"

    ТВОИ ВОЗМОЖНОСТИ:
    🏋️ Анализировать тренировки
    💬 Давать персональные советы  
    🎯 Помогать с целями
    🌟 Мотивировать
    📊 Оценивать прогресс

    ОТВЕЧАЙ КАК ДРУГ-ТРЕНЕР!
    """

    try:
        response = client.chat.completions.create(
            model="x-ai/grok-4.1-fast:free",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        # Запасные ответы
        fallback_responses = [
            "Отлично поработал! 💪 Продолжай в том же духе!",
            "Ты на правильном пути! 🚀 Горжусь твоим прогрессом!",
            "Каждая тренировка делает тебя сильнее! 🔥 Не сдавайся!",
            "Ты молодец! 🌟 Завтра будет еще лучше!"
        ]
        import random
        return random.choice(fallback_responses)


# === ОБРАБОТЧИКИ КОМАНД ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data[user.id] = {"workouts": 0, "goals": ["быть здоровым"]}

    welcome = f"""
Привет {user.first_name}! 👋 

Я твой ИИ-тренер Spovatar! 🤖
Просто расскажи мне о своих тренировках, и я:
• 🏋️ Проанализирую твой прогресс
• 💬 Дам персональный совет  
• 🌟 Помогу с мотивацией
• 🎯 Напомню о целях

Выбери действие ниже 👇
    """
    await update.message.reply_text(welcome, reply_markup=main_keyboard())


async def handle_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Увеличиваем счетчик тренировок
    if user_id not in user_data:
        user_data[user_id] = {"workouts": 0, "goals": []}
    user_data[user_id]["workouts"] += 1

    # ИИ анализирует тренировку
    response = await ai_fitness_coach(
        f"Пользователь завершил тренировку. Всего тренировок: {user_data[user_id]['workouts']}. Похвали и дай совет.",
        user_id
    )

    await update.message.reply_text(f"✅ Записал тренировку!\n\n{response}")


async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    workouts = user_data.get(user_id, {}).get("workouts", 0)

    response = await ai_fitness_coach(
        f"Пользователь спрашивает про свой прогресс. У него {workouts} тренировок. Оцени прогресс и мотивируй.",
        user_id
    )

    progress_text = f"📊 Твои тренировки: {workouts}\n\n{response}"
    await update.message.reply_text(progress_text)


async def handle_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    response = await ai_fitness_coach(
        "Дай персональный фитнес-совет на основе моего прогресса. Будь конкретным.",
        user_id
    )

    await update.message.reply_text(f"💬 Совет тренера:\n\n{response}")


async def handle_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    response = await ai_fitness_coach(
        "Дай мотивацию для продолжения тренировок. Будь эмоциональным и вдохновляющим.",
        user_id
    )

    await update.message.reply_text(f"🌟 Мотивация:\n\n{response}")


async def handle_goal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    response = await ai_fitness_coach(
        "Пользователь хочет поставить фитнес-цель. Помоги сформулировать реалистичную цель и план.",
        user_id
    )

    await update.message.reply_text(f"🎯 Постановка цели:\n\n{response}")


async def handle_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
🆘 Помощь по боту:

🏋️ *Записал тренировку* - отмечаешь факт тренировки
📊 *Мой прогресс* - смотрю твою статистику  
💬 *Совет тренера* - получаешь персональный совет
🌟 *Мотивация* - вдохновляю на новые свершения
🎯 *Поставить цель* - помогаю с целями

*Или просто пиши в чат:*
- "Сегодня бегал 5 км"
- "Силовая тренировка 45 минут" 
- "Как улучшить выносливость?"
- "Устал, нет мотивации"

Я все пойму и помогу! 💪
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка любых текстовых сообщений через ИИ"""
    user_id = update.effective_user.id
    user_text = update.message.text

    # Анализируем сообщение через ИИ
    response = await ai_fitness_coach(user_text, user_id)

    await update.message.reply_text(response)


# === ЗАПУСК БОТА ===
def main():
    application = Application.builder().token(bot_token).build()

    # Команды
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', handle_help))

    # Обработчики кнопок
    application.add_handler(MessageHandler(filters.Regex('^🏋️ Записал тренировку$'), handle_workout))
    application.add_handler(MessageHandler(filters.Regex('^📊 Мой прогресс$'), handle_progress))
    application.add_handler(MessageHandler(filters.Regex('^💬 Совет тренера$'), handle_advice))
    application.add_handler(MessageHandler(filters.Regex('^🌟 Мотивация$'), handle_motivation))
    application.add_handler(MessageHandler(filters.Regex('^🎯 Поставить цель$'), handle_goal))
    application.add_handler(MessageHandler(filters.Regex('^🆘 Помощь$'), handle_help))

    # Обработка любых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Фитнес-бот запущен!")
    application.run_polling()


if __name__ == "__main__":
    main()