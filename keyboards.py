from telegram import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo


def main_keyboard():
    buttons = [
        ['🏋️ Записал тренировку', '📊 Мой прогресс'],
        ['💬 Совет тренера', '🌟 Мотивация'],
        ['🎯 Поставить цель', '🆘 Помощь'],
        ['📱 Открыть приложение']  # Новая кнопка для мини-приложения
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def main_keyboard_with_webapp(web_app_url):
    """Клавиатура с кнопкой Web App"""
    web_app_button = KeyboardButton(
        "📱 Открыть приложение",
        web_app=WebAppInfo(url=web_app_url)
    )

    buttons = [
        ['🏋️ Записал тренировку', '📊 Мой прогресс'],
        ['💬 Совет тренера', '🌟 Мотивация'],
        ['🎯 Поставить цель', '🆘 Помощь'],
        [web_app_button]  # Кнопка Web App
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)


def workout_type_keyboard():
    buttons = [
        ['🚴 Велосипед', '🏃 Бег', '🏊 Плавание'],
        ['💪 Силовая', '🧘 Растяжка', '🎯 Другое']
    ]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)