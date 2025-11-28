from flask import Flask, request, jsonify, render_template
import os
import sys
import asyncio

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

# Используем ВСЕ ваши существующие модули!
from ai_coach import ai_fitness_coach
from user_data import get_user_data, update_user_workouts, get_user_workouts, add_user_goal


@app.route('/')
def index():
    """Главная страница мини-приложения для Telegram"""
    return open('index.html', 'r', encoding='utf-8').read()


@app.route('/ai-chat', methods=['POST'])
async def ai_chat():
    data = request.json
    user_message = data.get('message')
    user_id = data.get('user_id', 1)

    # Используем асинхронный вызов
    response = await ai_fitness_coach(user_message, user_id)
    return jsonify({'response': response})


@app.route('/add-workout', methods=['POST'])
def add_workout():
    data = request.json
    user_id = data.get('user_id', 1)
    workout_type = data.get('type')

    # Используем вашу готовую функцию!
    workouts_count = update_user_workouts(user_id, workout_type)
    return jsonify({'success': True, 'count': workouts_count})


@app.route('/get-progress', methods=['POST'])
def get_progress():
    data = request.json
    user_id = data.get('user_id', 1)

    workouts_count = get_user_workouts(user_id)
    return jsonify({'workouts': workouts_count})


@app.route('/set-goal', methods=['POST'])
def set_goal():
    data = request.json
    user_id = data.get('user_id', 1)
    goal_text = data.get('goal')

    if goal_text:
        add_user_goal(user_id, goal_text)
        return jsonify({'success': True, 'message': 'Цель установлена!'})

    return jsonify({'success': False, 'message': 'Ошибка установки цели'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)