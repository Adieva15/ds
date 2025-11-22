# === ПРОСТАЯ ПАМЯТЬ ===
user_data = {}  # Храним в оперативке: {user_id: {"workouts": 5, "goals": ["цель1", "цель2"]}}

def get_user_data(user_id):
    """Получить данные пользователя, создать если нет"""
    if user_id not in user_data:
        user_data[user_id] = {"workouts": 0, "goals": ["быть здоровым"]}
    return user_data[user_id]

def update_user_workouts(user_id):
    """Увеличить счетчик тренировок"""
    user_info = get_user_data(user_id)
    user_info["workouts"] += 1
    return user_info["workouts"]

def get_user_workouts(user_id):
    """Получить количество тренировок"""
    return get_user_data(user_id).get("workouts", 0)

def add_user_goal(user_id, goal):
    """Добавить цель пользователя"""
    user_info = get_user_data(user_id)
    if "goals" not in user_info:
        user_info["goals"] = []
    user_info["goals"].append(goal)

def get_user_goals(user_id):
    """Получить цели пользователя"""
    return get_user_data(user_id).get("goals", ["быть здоровым"])