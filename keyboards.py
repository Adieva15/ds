from telegram import ReplyKeyboardMarkup, KeyboardButton
def main_keyboard():
    buttons = [
        ['🏋️ Записал тренировку', '📊 Мой прогресс'],
        ['💬 Совет тренера', '🌟 Мотивация'],
        ['🎯 Поставить цель', '🆘 Помощь']
    ]

    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)