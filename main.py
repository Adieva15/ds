from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, ConversationHandler
from config import BOT_TOKEN, logger
from database import init_db
from handlers import (
    start, handle_help, handle_quick_workout, handle_progress,
    handle_advice, handle_motivation, handle_goal, handle_message,
    handle_workout, handle_workout_type, handle_workout_duration, handle_workout_distance,
    WORKOUT_TYPE, WORKOUT_DURATION, WORKOUT_DISTANCE
)


def setup_handlers(application):
    """Настройка всех обработчиков"""

    # Conversation Handler для записи тренировки
    workout_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^🏋️ Записать тренировку$'), handle_workout)],
        states={
            WORKOUT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_workout_type)],
            WORKOUT_DISTANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_workout_distance)],
            WORKOUT_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_workout_duration)],
        },
        fallbacks=[CommandHandler('cancel', start)]
    )

    # Команды
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', handle_help))

    # Обработчики
    application.add_handler(workout_conv_handler)
    application.add_handler(MessageHandler(filters.Regex('^📊 Мой прогресс$'), handle_progress))
    application.add_handler(MessageHandler(filters.Regex('^💬 Совет тренера$'), handle_advice))
    application.add_handler(MessageHandler(filters.Regex('^🌟 Мотивация$'), handle_motivation))
    application.add_handler(MessageHandler(filters.Regex('^🎯 Поставить цель$'), handle_goal))
    application.add_handler(MessageHandler(filters.Regex('^🆘 Помощь$'), handle_help))

    # Обработка любых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


def main():
    """Основная функция запуска бота"""
    init_db()
    logger.info("База данных инициализирована")

    application = Application.builder().token(BOT_TOKEN).build()
    setup_handlers(application)

    print("🤖 Кардио-бот запущен! (Велосипед 🚴, Бег 🏃, Плавание 🏊)")
    application.run_polling()


if __name__ == "__main__":
    main()