from aiogram.types import WebAppInfo
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config_reader import config

# main_markup = (
#     InlineKeyboardBuilder()
#     .button(text='🌐 Open Mini App', web_app=WebAppInfo(url=config.WEBAPP_URL))
#     .button(text='🏋️ Записал тренировку', callback_data='training_done')
#     .button(text='📊 Мой прогресс', callback_data='my_progress')
#     .button(text='💬 Совет тренера', callback_data='coach_advice')
#     .button(text='🎯 Поставить цель', callback_data='set_goal')
#     .adjust(2)  # 2 кнопки в каждом ряду
# ).as_markup()

main_markup = (
    InlineKeyboardBuilder()
    .button(text='🌐 Open Mini App', web_app=WebAppInfo(url=config.WEBAPP_URL))
).as_markup()

