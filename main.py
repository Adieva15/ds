from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from config import BOT_TOKEN
from handlers import (
    start, handle_help, handle_workout, handle_progress,
    handle_advice, handle_motivation, handle_goal, handle_message,
    #handle_webapp_message
)
from webapp_handler import handle_webapp_data, handle_mini_app_start


def setup_handlers(application):
    """Настройка всех обработчиков"""
    # Команды
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', handle_help))
    application.add_handler(CommandHandler('app', handle_mini_app_start))  # Новая команда для приложения

    # Обработчики кнопок
    application.add_handler(MessageHandler(filters.Regex('^🏋️ Записал тренировку$'), handle_workout))
    application.add_handler(MessageHandler(filters.Regex('^📊 Мой прогресс$'), handle_progress))
    application.add_handler(MessageHandler(filters.Regex('^💬 Совет тренера$'), handle_advice))
    application.add_handler(MessageHandler(filters.Regex('^🌟 Мотивация$'), handle_motivation))
    application.add_handler(MessageHandler(filters.Regex('^🎯 Поставить цель$'), handle_goal))
    application.add_handler(MessageHandler(filters.Regex('^🆘 Помощь$'), handle_help))
    application.add_handler(MessageHandler(filters.Regex('^📱 Открыть приложение$'), handle_mini_app_start))

    # Обработчик данных из Web App
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    # Обработка любых текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


def main():
    """Основная функция запуска бота"""
    application = Application.builder().token(BOT_TOKEN).build()

    setup_handlers(application)

    print("🤖 Фитнес-бот с мини-приложением запущен!")
    print("📱 Web App готов к работе!")
    print("💬 Бот принимает сообщения и данные из приложения...")

    application.run_polling()


if __name__ == "__main__":
    main()