from telegram import Update
from telegram.ext import ContextTypes
from ai_coach import ai_fitness_coach
from user_data import update_user_workouts, get_user_workouts, add_user_goal  # ⬅️ Импортируем из user_data.py
from keyboards import main_keyboard, main_keyboard_with_webapp
from config import WEB_APP_URL
import json


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    welcome = f"""
Привет {user.first_name}! 👋 

Я твой ИИ-тренер Spovatar! 🤖

📱 *Доступно в мини-приложении:*
• Удобная запись тренировок
• Детальная статистика  
• История прогресса
• Постановка целей

💬 *Или просто пиши мне:*
- О тренировках
- О целях
- За советом
- За мотивацией

Я все пойму и помогу! 💪
    """
    await update.message.reply_text(
        welcome,
        reply_markup=main_keyboard_with_webapp(WEB_APP_URL),
        parse_mode='Markdown'
    )


async def handle_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Увеличиваем счетчик тренировок
    workouts_count = update_user_workouts(user_id)

    # ИИ анализирует тренировку
    response = await ai_fitness_coach(
        f"Пользователь завершил тренировку. Всего тренировок: {workouts_count}. Похвали и дай конкретный совет.",
        user_id
    )

    await update.message.reply_text(f"✅ Записал тренировку!\n\n{response}")


async def handle_progress(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    workouts = get_user_workouts(user_id)

    response = await ai_fitness_coach(
        f"Пользователь спрашивает про свой прогресс. У него {workouts} тренировок. Оцени прогресс и мотивируй.",
        user_id
    )

    progress_text = f"📊 Твои тренировки: {workouts}\n\n{response}"
    await update.message.reply_text(progress_text)


async def handle_advice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    response = await ai_fitness_coach(
        "Дай персональный фитнес-совет на основе моего прогресса. Будь конкретным и практичным.",
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
- "Хочу похудеть/набрать массу"

Я все пойму и помогу! 💪
    """
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка любых текстовых сообщений через ИИ"""
    user_id = update.effective_user.id
    user_text = update.message.text

    # Автоматически определяем тренировки
    workout_keywords = ['трениров', 'бег', 'бегал', 'пробеж', 'велосипед', 'поездк', 'плаван', 'проплыл', 'отжимания',
                        'приседания', 'подтягивания']

    if any(keyword in user_text.lower() for keyword in workout_keywords):
        # Это описание тренировки - увеличиваем счетчик
        update_user_workouts(user_id)

    # Анализируем сообщение через ИИ
    response = await ai_fitness_coach(user_text, user_id)
    await update.message.reply_text(response)