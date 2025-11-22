import json
from telegram import Update
from telegram.ext import ContextTypes
from ai_coach import ai_fitness_coach
from user_data import update_user_workouts, add_user_goal  # ⬅️ Импортируем из user_data.py
from config import WEB_APP_URL
from keyboards import main_keyboard_with_webapp


async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка данных из Web App"""
    user_id = update.effective_user.id
    data = json.loads(update.effective_message.web_app_data.data)

    action = data.get('action')

    if action == 'workout':
        # Запись тренировки из мини-приложения
        workout_type = data.get('type', 'общая')
        duration = data.get('duration', 0)
        distance = data.get('distance', 0)

        # Увеличиваем счетчик
        workouts_count = update_user_workouts(user_id)

        # Генерируем ответ от ИИ
        response = await ai_fitness_coach(
            f"Пользователь завершил {workout_type} тренировку: {duration} минут, дистанция {distance}. Всего тренировок: {workouts_count}. Похвали и дай совет.",
            user_id
        )

        await update.message.reply_text(
            f"✅ Тренировка записана из приложения!\n"
            f"🏋️ Тип: {workout_type}\n"
            f"⏱️ Время: {duration} мин\n"
            f"📏 Дистанция: {distance}\n\n"
            f"{response}"
        )

    elif action == 'goal':
        # Установка цели из мини-приложения
        goal_text = data.get('goal', 'новая цель')
        add_user_goal(user_id, goal_text)

        response = await ai_fitness_coach(
            f"Пользователь поставил цель: {goal_text}. Поддержи и помоги с планом.",
            user_id
        )

        await update.message.reply_text(f"🎯 Цель установлена: {goal_text}\n\n{response}")

    elif action == 'message':
        # Произвольное сообщение из мини-приложения
        user_message = data.get('message', '')
        response = await ai_fitness_coach(user_message, user_id)
        await update.message.reply_text(response)


async def handle_mini_app_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка команды для открытия мини-приложения"""
    user = update.effective_user

    message = f"""
👋 Привет {user.first_name}!

Открой мини-приложение для удобного управления тренировками:

📱 *Возможности приложения:*
• Удобная запись тренировок
• Детальная статистика
• Постановка целей
• История прогресса

Нажми кнопку ниже чтобы открыть приложение 👇
    """

    await update.message.reply_text(
        message,
        reply_markup=main_keyboard_with_webapp(WEB_APP_URL),
        parse_mode='Markdown'
    )