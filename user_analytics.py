from datetime import datetime, timedelta
from sqlalchemy import func
from database import Workout, UserPreferences
from config import INACTIVITY_THRESHOLD_DAYS


class UserAnalytics:
    def __init__(self, db_session, user_id):
        self.db = db_session
        self.user_id = user_id

    def get_user_stats(self):
        """Получение статистики пользователя"""
        # Общее количество тренировок
        total_workouts = self.db.query(Workout).filter(Workout.user_id == self.user_id).count()

        # Тренировки за месяц
        month_ago = datetime.utcnow() - timedelta(days=30)
        month_workouts = self.db.query(Workout).filter(
            Workout.user_id == self.user_id,
            Workout.created_at >= month_ago
        ).count()

        # Тренировки за неделю
        week_ago = datetime.utcnow() - timedelta(days=7)
        week_workouts = self.db.query(Workout).filter(
            Workout.user_id == self.user_id,
            Workout.created_at >= week_ago
        ).count()

        # Последняя тренировка
        last_workout = self.db.query(Workout).filter(
            Workout.user_id == self.user_id
        ).order_by(Workout.created_at.desc()).first()

        inactivity_days = 0
        is_inactive = False

        if last_workout:
            inactivity_days = (datetime.utcnow() - last_workout.created_at).days
            is_inactive = inactivity_days > INACTIVITY_THRESHOLD_DAYS

        return {
            'total_workouts': total_workouts,
            'month_workouts': month_workouts,
            'week_workouts': week_workouts,
            'inactivity_days': inactivity_days,
            'is_inactive': is_inactive,
            'last_workout_date': last_workout.created_at if last_workout else None
        }

    def get_user_profile(self):
        """Получение профиля пользователя"""
        prefs = self.db.query(UserPreferences).filter(UserPreferences.user_id == self.user_id).first()

        if not prefs:
            # Создаем базовый профиль
            prefs = UserPreferences(
                user_id=self.user_id,
                fitness_level="начальный",
                preferred_workouts="Велосипед"
            )
            self.db.add(prefs)
            self.db.commit()

        stats = self.get_user_stats()

        # Определяем уровень подготовки
        if stats['total_workouts'] > 50:
            fitness_level = "продвинутый"
        elif stats['total_workouts'] > 20:
            fitness_level = "средний"
        else:
            fitness_level = "начальный"

        return {
            'fitness_level': fitness_level,
            'preferred_workouts': prefs.preferred_workouts,
            'injuries': prefs.injuries
        }

    def get_workout_trend(self):
        """Анализ тренда тренировок"""
        stats = self.get_user_stats()

        if stats['week_workouts'] > stats['month_workouts'] / 4:
            return "📈 Прогресс"
        elif stats['inactivity_days'] > 7:
            return "📉 Спад"
        else:
            return "➡️ Стабильно"

    def is_user_inactive(self):
        """Проверка неактивности пользователя"""
        stats = self.get_user_stats()
        return stats['is_inactive']