from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes, ConversationHandler
from sqlalchemy.orm import Session
from database import User, Workout, Goal, UserPreferences, get_db
from ai_coach import ai_fitness_coach, analyze_workout_pattern
from user_analytics import UserAnalytics
from keyboards import main_keyboard, workout_type_keyboard
from datetime import datetime

# Состояния для диалога записи тренировки
WORKOUT_TYPE, WORKOUT_DURATION, WORKOUT_DISTANCE = range(3)


async def handle_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начало диалога записи тренировки"""
    await update.message.reply_text(
        "🏋️ Выбери тип тренировки:",
        reply_markup=workout_type_keyboard()
    )
    return WORKOUT_TYPE


async def handle_workout_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка типа тренировки"""
    workout_type = update.message.text

    # Проверяем, что выбран допустимый тип тренировки
    valid_workouts = ['🚴 Велосипед', '🏃 Бег', '🏊 Плавание']
    if workout_type not in valid_workouts:
        await update.message.reply_text(
            "Пожалуйста, выбери тип тренировки из предложенных:",
            reply_markup=workout_type_keyboard()
        )
        return WORKOUT_TYPE

    context.user_data['workout_type'] = workout_type

    # Для разных типов тренировок разные единицы измерения
    if workout_type == '🚴 Велосипед':
        unit = "километров"
    elif workout_type == '🏃 Бег':
        unit = "километров"
    elif workout_type == '🏊 Плавание':
        unit = "метров"

    context.user_data['distance_unit'] = unit

    await update.message.reply_text(
        f"📏 Какая дистанция {unit}? (Введи число)",
        reply_markup=ReplyKeyboardMarkup([['Отмена']], resize_keyboard=True)
    )
    return WORKOUT_DISTANCE


async def handle_workout_distance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка дистанции тренировки"""
    if update.message.text == 'Отмена':
        await update.message.reply_text(
            "Отменил запись тренировки",
            reply_markup=main_keyboard()
        )
        return ConversationHandler.END

    try:
        distance = float(update.message.text)
        context.user_data['workout_distance'] = distance

        await update.message.reply_text(
            "⏱️ Сколько минут длилась тренировка?",
            reply_markup=ReplyKeyboardMarkup([['Отмена']], resize_keyboard=True)
        )
        return WORKOUT_DURATION
    except ValueError:
        await update.message.reply_text(
            f"Пожалуйста, введите число {context.user_data['distance_unit']}:"
        )
        return WORKOUT_DISTANCE


async def handle_workout_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Завершение записи тренировки"""
    if update.message.text == 'Отмена':
        await update.message.reply_text(
            "Отменил запись тренировки",
            reply_markup=main_keyboard()
        )
        return ConversationHandler.END

    user_id = update.effective_user.id

    try:
        duration = int(update.message.text)
    except ValueError:
        await update.message.reply_text("Пожалуйста, введите число минут:")
        return WORKOUT_DURATION

    with next(get_db()) as db:
        # Сохраняем тренировку в БД
        workout_type = context.user_data['workout_type']
        distance = context.user_data['workout_distance']
        unit = context.user_data['distance_unit']

        workout = Workout(
            user_id=user_id,
            workout_type=workout_type.replace('🚴 ', '').replace('🏃 ', '').replace('🏊 ', ''),
            duration=duration,
            intensity="средняя",  # Автоматически определяем по темпу
            notes=f"Дистанция: {distance} {unit}",
            distance=distance,
            distance_unit=unit
        )
        db.add(workout)
        db.commit()

        # Получаем аналитику
        analytics = UserAnalytics(db, user_id)
        stats = analytics.get_user_stats()

        # Генерируем УМНЫЙ ответ через ИИ
        user_message = f"Записал {workout_type} тренировку: {distance} {unit} за {duration} минут"

        response = await ai_fitness_coach(
            user_message,
            user_id,
            db,
            message_type="workout_completed"
        )

        # Добавляем анализ паттернов
        pattern_analysis = await analyze_workout_pattern(user_id, db)
        if pattern_analysis:
            response += f"\n\n📊 Анализ: {pattern_analysis}"

    await update.message.reply_text(
        f"✅ {workout_type} тренировка записана!\n\n{response}",
        reply_markup=main_keyboard()
    )
    return ConversationHandler.END


async def handle_quick_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Быстрая запись тренировки по кнопке (упрощенная)"""
    user_id = update.effective_user.id

    with next(get_db()) as db:
        # Создаем запись о тренировке с базовыми параметрами
        workout = Workout(
            user_id=user_id,
            workout_type="кардио",
            duration=30,
            intensity="средняя",
            notes="Быстрая запись через кнопку"
        )
        db.add(workout)
        db.commit()

        analytics = UserAnalytics(db, user_id)
        stats = analytics.get_user_stats()

        # Генерируем РАЗНЫЙ ответ каждый раз
        response = await ai_fitness_coach(
            f"Пользователь завершил кардио тренировку. Всего тренировок: {stats['total_workouts']}. "
            f"Дай КОНКРЕТНЫЙ совет по улучшению выносливости или техники.",
            user_id, db,
            message_type="workout_completed"
        )

    await update.message.reply_text(f"✅ Записал кардио тренировку!\n\n{response}")


async def handle_multiple_workouts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка запроса на запись нескольких тренировок"""
    user_id = update.effective_user.id
    user_text = update.message.text.lower()

    # Ищем цифры в сообщении
    import re
    numbers = re.findall(r'\d+', user_text)

    if numbers:
        workout_count = int(numbers[0])

        with next(get_db()) as db:
            for i in range(workout_count):
                # Чередуем типы тренировок
                workout_types = ['Велосипед', 'Бег', 'Плавание']
                workout_type = workout_types[i % 3]

                workout = Workout(
                    user_id=user_id,
                    workout_type=workout_type,
                    duration=45,
                    intensity="средняя",
                    notes=f"Записано пакетом: {workout_count} тренировок"
                )
                db.add(workout)
            db.commit()

            analytics = UserAnalytics(db, user_id)
            stats = analytics.get_user_stats()

            response = await ai_fitness_coach(
                f"Пользователь записал {workout_count} тренировок (велосипед, бег, плавание). "
                f"Всего теперь {stats['total_workouts']}. "
                f"Проанализируй кардио нагрузку и дай РЕАЛЬНЫЙ совет по восстановлению.",
                user_id, db,
                message_type="workout_completed"
            )

        await update.message.reply_text(
            f"✅ Записал {workout_count} тренировок (велосипед, бег, плавание)!\n\n{response}"
        )
    else:
        await update.message.reply_text(
            "Сколько именно тренировок записать? Напиши, например: 'записать 2 тренировки'"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработка любых текстовых сообщений через ИИ"""
    user_id = update.effective_user.id
    user_text = update.message.text

    # Проверяем, не является ли сообщение командой записи тренировки
    if any(word in user_text.lower() for word in ['велосипед', 'бег', 'плавание', 'пробежал', 'проехал', 'проплыл']):
        # Это описание тренировки - обрабатываем через ИИ
        with next(get_db()) as db:
            # Сначала проверяем неактивность
            analytics = UserAnalytics(db, user_id)
            if analytics.is_user_inactive():
                reminder = await generate_motivational_reminder(user_id, db)
                if reminder:
                    await update.message.reply_text(f"💌 Напоминание: {reminder}")

            # Анализируем сообщение через ИИ
            response = await ai_fitness_coach(user_text, user_id, db, message_type="workout_description")

        await update.message.reply_text(response)
    else:
        # Обычное сообщение
        with next(get_db()) as db:
            response = await ai_fitness_coach(user_text, user_id, db, message_type="general")
        await update.message.reply_text(response)