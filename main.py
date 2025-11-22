import logging
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters
from openai import OpenAI
import sqlite3
from datetime import datetime, timedelta
import random

# Настройки
ai_token = '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'
bot_token = '7971545933:AAHJpI7CzpfvlYVF5y9liUqx4RyjDMJbmPA'

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# База данных
class FitnessDB:
    def __init__(self):
        self.conn = sqlite3.connect('fitness.db', check_same_thread=False)
        self.init_db()

    def init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                username TEXT,
                first_name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS workouts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                duration INTEGER,
                type TEXT,
                calories INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS streaks (
                user_id INTEGER PRIMARY KEY,
                current_streak INTEGER DEFAULT 0,
                best_streak INTEGER DEFAULT 0,
                last_activity DATE
            )
        ''')
        self.conn.commit()

    def add_user(self, user_id, username, first_name):
        cursor = self.conn.cursor()
        cursor.execute('INSERT OR IGNORE INTO users (user_id, username, first_name) VALUES (?, ?, ?)',
                       (user_id, username, first_name))
        cursor.execute('INSERT OR IGNORE INTO streaks (user_id) VALUES (?)', (user_id,))
        self.conn.commit()

    def add_workout(self, user_id, duration, workout_type, calories):
        cursor = self.conn.cursor()
        cursor.execute('INSERT INTO workouts (user_id, duration, type, calories) VALUES (?, ?, ?, ?)',
                       (user_id, duration, workout_type, calories))

        # Обновляем стрик
        today = datetime.now().date()
        cursor.execute('SELECT last_activity, current_streak, best_streak FROM streaks WHERE user_id = ?', (user_id,))
        result = cursor.fetchone()

        if result:
            last_activity, current_streak, best_streak = result
            last_activity = datetime.strptime(last_activity, '%Y-%m-%d').date() if last_activity else None

            if not last_activity or last_activity < today - timedelta(days=1):
                new_streak = 1
            elif last_activity == today - timedelta(days=1):
                new_streak = current_streak + 1
            else:
                new_streak = current_streak

            new_best_streak = max(new_streak, best_streak)

            cursor.execute(
                'UPDATE streaks SET current_streak = ?, best_streak = ?, last_activity = ? WHERE user_id = ?',
                (new_streak, new_best_streak, today, user_id))

        self.conn.commit()

    def get_user_stats(self, user_id):
        cursor = self.conn.cursor()

        cursor.execute('SELECT COUNT(*) FROM workouts WHERE user_id = ?', (user_id,))
        total_workouts = cursor.fetchone()[0]

        cursor.execute('SELECT AVG(duration) FROM workouts WHERE user_id = ?', (user_id,))
        avg_duration = cursor.fetchone()[0] or 0

        cursor.execute('SELECT current_streak, best_streak FROM streaks WHERE user_id = ?', (user_id,))
        streak_data = cursor.fetchone()
        current_streak = streak_data[0] if streak_data else 0
        best_streak = streak_data[1] if streak_data else 0

        week_ago = (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')
        cursor.execute('SELECT COUNT(*) FROM workouts WHERE user_id = ? AND created_at >= ?', (user_id, week_ago))
        weekly_workouts = cursor.fetchone()[0]

        return {
            'total_workouts': total_workouts,
            'avg_duration': round(avg_duration, 1),
            'current_streak': current_streak,
            'best_streak': best_streak,
            'weekly_workouts': weekly_workouts
        }


# Инициализация базы данных
db = FitnessDB()


# Клавиатуры
def create_main_keyboard():
    keyboard = [
        [KeyboardButton('🏋️ Добавить тренировку'), KeyboardButton('📊 Моя статистика')],
        [KeyboardButton('💬 Чат с тренером'), KeyboardButton('🎯 Мои цели')],
        [KeyboardButton('🌟 Мотивация'), KeyboardButton('⚡ Быстрая тренировка')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def create_workout_keyboard():
    keyboard = [
        [KeyboardButton('💪 Силовая'), KeyboardButton('🏃 Кардио')],
        [KeyboardButton('🧘 Йога'), KeyboardButton('🏊 Плавание')],
        [KeyboardButton('⬅️ Назад')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def create_duration_keyboard():
    keyboard = [
        [KeyboardButton('15 мин'), KeyboardButton('30 мин')],
        [KeyboardButton('45 мин'), KeyboardButton('60 мин')],
        [KeyboardButton('90+ мин'), KeyboardButton('⬅️ Назад')]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


# ИИ функции
async def generate_fitness_response(prompt, user_stats=None):
    """Генерация ответа от фитнес-тренера"""

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=ai_token,
    )

    context = ""
    if user_stats:
        context = f"""
        Контекст пользователя:
        - Тренировок всего: {user_stats['total_workouts']}
        - Текущая серия: {user_stats['current_streak']} дней
        - Тренировок за неделю: {user_stats['weekly_workouts']}
        - Средняя продолжительность: {user_stats['avg_duration']} минут
        """

    system_prompt = f"""Ты - виртуальный фитнес-тренер Spovatar. Ты дружелюбный, мотивирующий и эмоциональный. 
Отвечай кратко (1-2 предложения), используй эмодзи. Будь поддерживающим и заботливым.

{context}

Твой стиль:
- Используй фитнес-сленг 🏋️
- Будь эмоциональным 😊🎉💪
- Хвали за достижения
- Поддерживай при неудачах
- Давай практические советы"""

    try:
        completion = client.chat.completions.create(
            model="x-ai/grok-4.1-fast:free",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка ИИ: {e}")
        return get_fallback_response(prompt)


def get_fallback_response(prompt):
    """Запасные ответы если ИИ не работает"""
    text_lower = prompt.lower()

    # Реакции на тренировки
    if any(word in text_lower for word in ['тренировка', 'занимался', 'потренировался', 'спорт']):
        responses = [
            "Отличная работа! 💪 Ты становишься сильнее с каждой тренировкой!",
            "Супер! 🚀 Регулярность - ключ к успеху в фитнесе!",
            "Молодец! 🌟 Помни: даже небольшие тренировки ведут к большим результатам!",
            "Круто! 🔥 Твое тело благодарит тебя за эту работу!"
        ]
        return random.choice(responses)

    # Мотивация
    elif any(word in text_lower for word in ['устал', 'нет сил', 'лень', 'усталость']):
        responses = [
            "Я понимаю! 💙 Иногда бывают такие дни. Главное - не сдаваться!",
            "Отдохни немного! 🛌 Восстановление - важная часть тренировочного процесса!",
            "Слушай свое тело! 👂 Если нужно - отдохни, но завтра обязательно продолжи!",
            "Ты сильнее чем думаешь! 💪 Просто сделай небольшое усилие!"
        ]
        return random.choice(responses)

    # Советы
    elif any(word in text_lower for word in ['совет', 'рекомендация', 'как тренироваться']):
        responses = [
            "Советую добавить разнообразия в тренировки! 🔄 Попробуй новые упражнения!",
            "Не забывай про растяжку после тренировки! 🧘 Это улучшит гибкость!",
            "Пей больше воды во время тренировок! 💧 Гидратация очень важна!",
            "Чередуй силовые и кардио тренировки! ⚖️ Это даст лучший результат!"
        ]
        return random.choice(responses)

    else:
        responses = [
            "Отличный вопрос! 💭 Продолжай в том же духе!",
            "Интересно! 🤔 Давай обсудим это подробнее!",
            "Спасибо за вопрос! 🌟 Я всегда рад помочь с тренировками!",
            "Отлично! 🎯 Давай работать над твоими фитнес-целями вместе!"
        ]
        return random.choice(responses)


# Обработчики команд
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    db.add_user(user.id, user.username, user.first_name)

    welcome_text = f"""
Привет, {user.first_name}! 👋 

Я твой виртуальный фитнес-тренер Spovatar! 🤖

Я помогу тебе:
🏋️ Отслеживать тренировки
📊 Анализировать прогресс  
💬 Давать персональные советы
🎯 Достигать твоих целей

Выбери действие ниже 👇
    """
    await update.message.reply_text(welcome_text, reply_markup=create_main_keyboard())


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """🤖 *Как пользоваться ботом:*

🏋️ *Добавить тренировку* - записать новую тренировку
📊 *Моя статистика* - посмотреть прогресс
💬 *Чат с тренером* - задать вопрос ИИ-тренеру
🎯 *Мои цели* - поставить фитнес-цели
🌟 *Мотивация* - получить мотивацию
⚡ *Быстрая тренировка* - экспресс-комплекс

*Примеры запросов для чата:*
• "Как улучшить выносливость?"
• "Сколько отдыхать между тренировками?"
• "Посоветуй упражнения для пресса"
• "Я устал, что делать?""""

    await update.message.reply_text(help_text, parse_mode='Markdown')


async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stats = db.get_user_stats(user_id)

    stats_text = f"""
📊 *Твоя фитнес-статистика:*

🏋️ Всего тренировок: *{stats['total_workouts']}*
⏱️ Средняя продолжительность: *{stats['avg_duration']} мин*
🔥 Текущая серия: *{stats['current_streak']} дней*
🏆 Лучшая серия: *{stats['best_streak']} дней*
📅 На этой неделе: *{stats['weekly_workouts']} тренировок*

*Ты молодец! Продолжай в том же духе!* 💪
    """

    # Добавляем персональный совет
    advice_prompt = f"Пользователь имеет статистику: {stats}. Дай краткий мотивирующий совет."
    advice = await generate_fitness_response(advice_prompt, stats)

    await update.message.reply_text(stats_text + f"\n💡 *Совет тренера:* {advice}",
                                    parse_mode='Markdown')


# Обработчики кнопок
async def handle_add_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Выбери тип тренировки: 💪",
        reply_markup=create_workout_keyboard()
    )


async def handle_workout_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    workout_type = update.message.text
    context.user_data['workout_type'] = workout_type
    await update.message.reply_text(
        f"Отлично! {workout_type} - это здорово! 🎯\nСколько минут длилась тренировка?",
        reply_markup=create_duration_keyboard()
    )


async def handle_workout_duration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    duration_text = update.message.text
    duration = int(''.join(filter(str.isdigit, duration_text)))
    workout_type = context.user_data.get('workout_type', 'общая')

    # Расчет калорий (примерный)
    calories = duration * 7

    # Сохраняем тренировку
    db.add_workout(user_id, duration, workout_type, calories)

    # Получаем статистику для контекста
    stats = db.get_user_stats(user_id)

    # Генерируем реакцию ИИ
    prompt = f"Пользователь только что завершил {workout_type} тренировку длительностью {duration} минут. Отреагируй эмоционально и поддержи его."
    reaction = await generate_fitness_response(prompt, stats)

    response = f"""
🎉 *Тренировка сохранена!*

{reaction}

📝 *Детали:*
⏱️ Длительность: {duration} минут
💪 Тип: {workout_type} 
🔥 Сожжено: ~{calories} калорий

📊 *Обновленная статистика:*
Всего тренировок: {stats['total_workouts'] + 1}
Текущая серия: {stats['current_streak']} дней
    """

    await update.message.reply_text(response, parse_mode='Markdown', reply_markup=create_main_keyboard())


async def handle_motivation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stats = db.get_user_stats(user_id)

    prompt = "Дай мотивирующее сообщение для пользователя который занимается фитнесом. Будь эмоциональным и вдохновляющим."
    motivation = await generate_fitness_response(prompt, stats)

    await update.message.reply_text(f"🌟 *Мотивация от тренера:*\n\n{motivation}",
                                    parse_mode='Markdown')


async def handle_quick_workout(update: Update, context: ContextTypes.DEFAULT_TYPE):
    quick_workouts = [
        "⚡ *Быстрая тренировка на 10 минут:*\n• 20 приседаний\n• 15 отжиманий\n• 30 сек планка\n• 20 скручиваний\n• Повтори 2 круга! 💨",
        "🔥 *Экспресс-комплекс на 15 минут:*\n• 30 прыжков\n• 15 выпадов\n• 20 скручиваний\n• 10 берпи\n• 30 сек планка\n• 3 круга! 🚀",
        "💪 *Силовой экспресс:*\n• 25 приседаний\n• 20 отжиманий\n• 15 подъемов корпуса\n• 10 обратных отжиманий\n• 2 минуты планки\n• Не останавливайся! 🔥"
    ]

    workout = random.choice(quick_workouts)
    await update.message.reply_text(workout, parse_mode='Markdown')


async def handle_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "💬 *Чат с тренером активирован!*\n\nЗадай мне любой вопрос о тренировках, питании или мотивации! Я всегда готов помочь! 🏋️‍♂️\n\n_Просто напиши свой вопрос..._",
        parse_mode='Markdown'
    )


async def handle_goals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    goals_text = """
🎯 *Постановка целей*

В разработке! Скоро здесь ты сможешь:
• Ставить фитнес-цели
• Отслеживать прогресс
• Получать награды за достижения

А пока просто продолжай тренироваться! 💪
    """
    await update.message.reply_text(goals_text, parse_mode='Markdown')


async def handle_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Возвращаемся в главное меню:",
        reply_markup=create_main_keyboard()
    )


# Основной обработчик сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    user_id = update.effective_user.id

    # Получаем статистику для контекста
    stats = db.get_user_stats(user_id)

    # Генерируем ответ через ИИ
    response = await generate_fitness_response(user_text, stats)

    await update.message.reply_text(response, parse_mode='Markdown')


def main():
    try:
        logger.info("Запуск фитнес-бота...")
        application = Application.builder().token(bot_token).build()

        # Команды
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('help', help_command))
        application.add_handler(CommandHandler('stats', stats_command))

        # Обработчики кнопок
        application.add_handler(MessageHandler(filters.Regex('^🏋️ Добавить тренировку$'), handle_add_workout))
        application.add_handler(MessageHandler(filters.Regex('^📊 Моя статистика$'), stats_command))
        application.add_handler(MessageHandler(filters.Regex('^💬 Чат с тренером$'), handle_chat))
        application.add_handler(MessageHandler(filters.Regex('^🎯 Мои цели$'), handle_goals))
        application.add_handler(MessageHandler(filters.Regex('^🌟 Мотивация$'), handle_motivation))
        application.add_handler(MessageHandler(filters.Regex('^⚡ Быстрая тренировка$'), handle_quick_workout))
        application.add_handler(MessageHandler(filters.Regex('^⬅️ Назад$'), handle_back))

        # Типы тренировок
        application.add_handler(
            MessageHandler(filters.Regex('^(💪 Силовая|🏃 Кардио|🧘 Йога|🏊 Плавание)$'), handle_workout_type))

        # Длительность тренировок
        application.add_handler(MessageHandler(filters.Regex('.*мин$'), handle_workout_duration))

        # Обработка обычных сообщений
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

        logger.info("Фитнес-бот запущен!")
        application.run_polling()

    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    main()

