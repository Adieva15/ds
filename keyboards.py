from telegram import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    buttons = [
        ['🏋️ Записать тренировку', '📊 Мой прогресс'],
        ['💬 Совет тренера', '🌟 Мотивация'],
        ['🎯 Поставить цель', '🆘 Помощь']
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def workout_type_keyboard():
    buttons = [
        ['🚴 Велосипед', '🏃 Бег'],
        ['🏊 Плавание']
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)