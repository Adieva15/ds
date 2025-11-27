from flask import Flask, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = Flask(__name__)

# Используем ВСЕ ваши существующие модули!
from ai_coach import ai_fitness_coach
from user_data import get_user_data, update_user_workouts

@app.route('/')
def index():
    """Главная страница мини-приложения"""
    return open('templates/index.html', 'r', encoding='utf-8').read()

@app.route('/ai-chat', methods=['POST'])
def ai_chat():
    data = request.json
    user_message = data.get('message')
    user_id = data.get('user_id', 1)
    response = ai_fitness_coach(user_message, user_id)
    return jsonify({'response': response})


@app.route('/add-workout', methods=['POST'])
def add_workout():
    data = request.json
    user_id = data.get('user_id')
    workout_type = data.get('type')

    # Используем вашу готовую функцию!
    workouts_count = update_user_workouts(user_id, workout_type)
    return jsonify({'success': True, 'count': workouts_count})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)