# mini_app.py - версия для PythonAnywhere
from flask import Flask, request, jsonify
import os
import sys

# Добавляем путь к модулям
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Импортируем только необходимые функции
try:
    from user_data import get_user_data, update_user_workouts
    from ai_coach import ai_fitness_coach

    AI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Некоторые модули недоступны: {e}")
    AI_AVAILABLE = False


def simple_ai_response(message):
    """Простой ответ без ИИ"""
    responses = {
        'привет': 'Привет! Я ваш фитнес-помощник! 💪',
        'прогресс': 'Посмотрите свой прогресс в разделе статистики! 📊',
        'тренировка': 'Отличная работа! Продолжайте в том же духе! 🏋️',
        'цель': 'Ставьте реалистичные цели и достигайте их! 🎯',
        'мотивация': 'Вы делаете великие дела! Не сдавайтесь! 🔥'
    }

    message_lower = message.lower()
    for key, response in responses.items():
        if key in message_lower:
            return response

    return "Спасибо за сообщение! Сейчас я работаю в упрощенном режиме. 🏃"


@app.route('/')
def index():
    """Главная страница мини-приложения"""
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Spovatar - Фитнес-тренер</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 15px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        .container {
            max-width: 400px;
            margin: 0 auto;
        }
        .card {
            background: white;
            padding: 15px;
            margin: 10px 0;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .btn {
            background: #0088cc;
            color: white;
            padding: 12px;
            margin: 5px 0;
            border-radius: 8px;
            text-align: center;
            cursor: pointer;
            border: none;
            width: 100%;
            font-size: 16px;
        }
        .btn:hover {
            background: #0066aa;
        }
        .status {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 10px;
            text-align: center;
            font-weight: bold;
        }
        .ai-on { background: #d4edda; color: #155724; }
        .ai-off { background: #f8d7da; color: #721c24; }
        .chat-message {
            padding: 8px;
            margin: 5px 0;
            border-radius: 8px;
        }
        .user-msg { background: #e3f2fd; text-align: right; }
        .bot-msg { background: #f5f5f5; }
    </style>
</head>
<body>
    <div class="container">
        <div style="text-align: center; color: white; margin-bottom: 20px;">
            <h1>🤖 Spovatar Mini</h1>
            <p>Ваш фитнес-помощник</p>
        </div>

        <div id="status" class="status"></div>

        <div class="card">
            <h3>🏋️ Быстрые действия</h3>
            <button class="btn" onclick="addWorkout('бег')">🏃 Записать бег</button>
            <button class="btn" onclick="addWorkout('велосипед')">🚴 Записать велосипед</button>
            <button class="btn" onclick="addWorkout('плавание')">🏊 Записать плавание</button>
            <button class="btn" onclick="addWorkout('силовая')">💪 Записать силовую</button>
        </div>

        <div class="card">
            <h3>📊 Мой прогресс</h3>
            <div id="progress">Загрузка...</div>
            <button class="btn" onclick="loadProgress()">🔄 Обновить</button>
        </div>

        <div class="card">
            <h3>💬 Чат с тренером</h3>
            <input type="text" id="messageInput" placeholder="Ваш вопрос..." 
                   style="width: 100%; padding: 10px; margin: 5px 0; border: 1px solid #ddd; border-radius: 5px;">
            <button class="btn" onclick="sendMessage()">📨 Отправить</button>
            <div id="chat" style="margin-top: 10px; max-height: 200px; overflow-y: auto;"></div>
        </div>
    </div>

    <script>
        // Инициализация Telegram Web App
        const tg = window.Telegram.WebApp;
        tg.expand();
        tg.ready();

        // Показываем статус
        document.getElementById('status').className = 'status ' + (''' + str(AI_AVAILABLE).lower() + ''' ? 'ai-on' : 'ai-off');
        document.getElementById('status').textContent = ''' + str(AI_AVAILABLE).lower() + ''' ? 
            '✅ ИИ-тренер доступен' : '⚠️ Упрощенный режим';

        // Загружаем прогресс при старте
        loadProgress();

        async function loadProgress() {
            try {
                const userId = tg.initDataUnsafe.user?.id || 1;
                const response = await fetch('/progress?user_id=' + userId);
                const data = await response.json();

                if (data.success) {
                    document.getElementById('progress').innerHTML = `
                        <strong>Всего тренировок:</strong> ${data.workouts}<br>
                        <strong>Активные цели:</strong> ${data.goals}
                    `;
                } else {
                    document.getElementById('progress').innerHTML = `
                        <strong>Всего тренировок:</strong> ${data.workouts || 0}<br>
                        <strong>Цель:</strong> стать сильнее 💪
                    `;
                }
            } catch (error) {
                document.getElementById('progress').innerHTML = 'Ошибка загрузки данных';
            }
        }

        async function addWorkout(type) {
            try {
                const userId = tg.initDataUnsafe.user?.id || 1;
                const response = await fetch('/add-workout', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_id: userId,
                        type: type
                    })
                });

                const data = await response.json();
                if (data.success) {
                    addChatMessage(`✅ Записал ${type}! Всего тренировок: ${data.count}`, 'bot');
                    loadProgress();
                } else {
                    addChatMessage('❌ Ошибка записи', 'bot');
                }
            } catch (error) {
                addChatMessage('❌ Ошибка соединения', 'bot');
            }
        }

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            addChatMessage('Вы: ' + message, 'user');
            input.value = '';

            try {
                const userId = tg.initDataUnsafe.user?.id || 1;
                const response = await fetch('/ai-chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        user_id: userId,
                        message: message
                    })
                });

                const data = await response.json();
                addChatMessage('Тренер: ' + data.response, 'bot');
            } catch (error) {
                addChatMessage('Тренер: Ошибка соединения', 'bot');
            }
        }

        function addChatMessage(text, sender) {
            const chat = document.getElementById('chat');
            const msg = document.createElement('div');
            msg.className = 'chat-message ' + (sender === 'user' ? 'user-msg' : 'bot-msg');
            msg.textContent = text;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }

        // Отправка по Enter
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
    '''


@app.route('/progress')
def progress():
    """Получение прогресса пользователя"""
    try:
        user_id = request.args.get('user_id', type=int, default=1)
        if AI_AVAILABLE:
            user_data = get_user_data(user_id)
            return jsonify({
                'success': True,
                'workouts': user_data.get('workouts', 0),
                'goals': ', '.join(user_data.get('goals', ['стать сильнее']))
            })
        else:
            return jsonify({
                'success': False,
                'workouts': 0,
                'goals': 'стать сильнее'
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'workouts': 0,
            'goals': 'стать сильнее'
        })


@app.route('/add-workout', methods=['POST'])
def add_workout():
    """Добавление тренировки"""
    try:
        data = request.json
        user_id = data.get('user_id', 1)
        workout_type = data.get('type', 'тренировка')

        if AI_AVAILABLE:
            count = update_user_workouts(user_id, workout_type)
            return jsonify({'success': True, 'count': count})
        else:
            # Эмуляция в памяти для демо
            return jsonify({'success': True, 'count': 1})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    """Чат с тренером"""
    try:
        data = request.json
        user_message = data.get('message', '')
        user_id = data.get('user_id', 1)

        if not user_message:
            return jsonify({'response': 'Напишите ваше сообщение'})

        if AI_AVAILABLE:
            # Используем асинхронный вызов
            import asyncio
            response = asyncio.run(ai_fitness_coach(user_message, user_id))
        else:
            response = simple_ai_response(user_message)

        return jsonify({'response': response})

    except Exception as e:
        return jsonify({'response': 'Извините, произошла ошибка. Попробуйте позже.'})


if __name__ == '__main__':
    app.run(debug=True)