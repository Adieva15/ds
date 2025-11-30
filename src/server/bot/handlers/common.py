from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from bot.keyboards import main_markup
from db import User

router = Router(name='common')

@router.message(CommandStart())
async def start(message:Message)->None:
    # создает нового пользователя, возвр тру или фолс
    user = await User.filter(id=message.from_user.id).exists()
    if not user:
        await User.create(id=message.from_user.id, name=message.from_user.first_name)

    await message.answer("Open My First Mini App", reply_markup=main_markup)

# from aiogram import Router, F
# from aiogram.types import Message
# from aiogram.filters import CommandStart, Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup

# from bot.keyboards import main_markup, main_keyboard
# from db import User
# from server.bot.aii.ai_coach import ai_fitness_coach

# router = Router(name='common')

# # Состояния для FSM
# class UserStates(StatesGroup):
#     waiting_workout_type = State()
#     waiting_for_goal = State()

# # === ОБРАБОТЧИКИ КОМАНД ===

# @router.message(CommandStart())
# async def start(message: Message):
#     """Обработчик команды /start"""
#     user_id = message.from_user.id
#     username = message.from_user.username
#     first_name = message.from_user.first_name
    
#     # Создаем или получаем пользователя
#     user, created = await User.get_or_create(
#         telegram_id=user_id,
#         defaults={
#             'username': username,
#             'full_name': first_name
#         }
#     )
    
#     welcome = f"""
# Привет {first_name}! 👋 

# Я твой ИИ-тренер Spovatar! 🤖
# Просто расскажи мне о своих тренировках, и я:
# • 🏋️ Проанализирую твой прогресс
# • 💬 Дам персональный совет  
# • 🌟 Помогу с мотивацией
# • 🎯 Напомню о целях

# Выбери действие ниже 👇
#     """
#     await message.answer(welcome, reply_markup=main_keyboard())

# # === ОБРАБОТЧИКИ КНОПОК ===

# @router.message(F.text == "🏋️ Записал тренировку")
# async def handle_workout(message: Message, state: FSMContext):
#     """Обработчик кнопки записи тренировки"""
#     await message.answer(
#         "Какой тип тренировки?\n\n"
#         "🏃 Бег\n"
#         "🚴 Велосипед\n"
#         "🏊 Плавание"
#     )
#     await state.set_state(UserStates.waiting_workout_type)

# @router.message(F.text == "📊 Мой прогресс")
# async def handle_progress(message: Message):
#     """Обработчик кнопки прогресса"""
#     user_id = message.from_user.id
#     user = await User.get(telegram_id=user_id)
    
#     workouts_count = user.workouts_count if hasattr(user, 'workouts_count') else 0
    
#     response = await ai_fitness_coach(
#         f"Пользователь спрашивает про свой прогресс. У него {workouts_count} тренировок. Оцени прогресс и мотивируй.",
#         user_id
#     )
    
#     progress_text = f"📊 Твои тренировки: {workouts_count}\n\n{response}"
#     await message.answer(progress_text)

# @router.message(F.text == "💬 Совет тренера")
# async def handle_advice(message: Message):
#     """Обработчик кнопки совета тренера"""
#     user_id = message.from_user.id
    
#     response = await ai_fitness_coach(
#         "Дай персональный фитнес-совет на основе моего прогресса. Будь конкретным.",
#         user_id
#     )
    
#     await message.answer(f"💬 Совет тренера:\n\n{response}")

# @router.message(F.text == "🌟 Мотивация")
# async def handle_motivation(message: Message):
#     """Обработчик кнопки мотивации"""
#     user_id = message.from_user.id
    
#     response = await ai_fitness_coach(
#         "Дай мотивацию для продолжения тренировок. Будь эмоциональным и вдохновляющим.",
#         user_id
#     )
    
#     await message.answer(f"🌟 Мотивация:\n\n{response}")

# @router.message(F.text == "🎯 Поставить цель")
# async def handle_goal(message: Message, state: FSMContext):
#     """Обработчик кнопки постановки цели"""
#     await message.answer(
#         "🎯 Какую фитнес-цель ты хочешь поставить?\n\n"
#         "Например:\n"
#         "• 'Пробежать 5 км без остановки'\n"
#         "• 'Проплыть 500 метров'\n"
#         "• 'Проехать 20 км на велосипеде'"
#     )
#     await state.set_state(UserStates.waiting_for_goal)

# @router.message(F.text == "🆘 Помощь")
# async def handle_help(message: Message):
#     """Обработчик кнопки помощи"""
#     help_text = """
# 🆘 Помощь по боту:

# 🏋️ *Записал тренировку* - отмечаешь факт тренировки
# 📊 *Мой прогресс* - смотрю твою статистику  
# 💬 *Совет тренера* - получаешь персональный совет
# 🌟 *Мотивация* - вдохновляю на новые свершения
# 🎯 *Поставить цель* - помогаю с целями

# *Или просто пиши в чат:*
# - "Сегодня бегал 5 км"
# - "Плавал 30 минут" 
# - "Как улучшить выносливость?"
# - "Устал, нет мотивации"

# Я все пойму и помогу! 💪
#     """
#     await message.answer(help_text)

# # === ОБРАБОТЧИКИ СОСТОЯНИЙ ===

# @router.message(UserStates.waiting_workout_type)
# async def process_workout_type(message: Message, state: FSMContext):
#     """Обработка выбора типа тренировки"""
#     user_id = message.from_user.id
#     user_text = message.text.lower()
    
#     workout_type = None
#     if any(word in user_text for word in ['бег', 'run']):
#         workout_type = "бег"
#     elif any(word in user_text for word in ['велосипед', 'вело', 'bike']):
#         workout_type = "велосипед"
#     elif any(word in user_text for word in ['плавание', 'плыл', 'swim']):
#         workout_type = "плавание"

#     if workout_type:
#         # Обновляем счетчик тренировок
#         user = await User.get(telegram_id=user_id)
#         user.workouts_count = getattr(user, 'workouts_count', 0) + 1
#         await user.save()
        
#         response = await ai_fitness_coach(
#             f"Завершил {workout_type}. Всего тренировок: {user.workouts_count}", 
#             user_id
#         )
#         await message.answer(f"✅ Записал {workout_type}! Всего: {user.workouts_count}\n\n{response}")
#     else:
#         await message.answer("Не понял тип тренировки. Выбери: бег, велосипед или плавание")
    
#     await state.clear()

# @router.message(UserStates.waiting_for_goal)
# async def process_goal(message: Message, state: FSMContext):
#     """Обработка постановки цели"""
#     user_id = message.from_user.id
#     user_text = message.text
    
#     try:
#         # Сохраняем цель в базу
#         user = await User.get(telegram_id=user_id)
#         user.goal = user_text
#         await user.save()
        
#         response = f"🎯 Отлично! Цель '{user_text}' сохранена!\n\nТеперь давай работать над её достижением! 💪"
#     except Exception as e:
#         response = "❌ Не удалось сохранить цель. Попробуй еще раз."
    
#     await message.answer(response)
#     await state.clear()

# # === ОБРАБОТЧИК ЛЮБЫХ СООБЩЕНИЙ ===

# @router.message()
# async def handle_message(message: Message):
#     """Обработка любых текстовых сообщений через ИИ"""
#     user_id = message.from_user.id
#     user_text = message.text
    
#     response = await ai_fitness_coach(user_text, user_id)
#     await message.answer(response)