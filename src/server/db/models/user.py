#указывает поля
from tortoise import fields
# для наследования модели
from tortoise.models import Model
# для перевода таблицы в json
from tortoise.contrib.pydantic import pydantic_model_creator


class User(Model):
    id = fields.BigIntField(pk=True)
    telegram_id = fields.BigIntField(unique=True)
    username = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255)
    workouts_count = fields.IntField(default=0)
    goal = fields.TextField(null=True)
    # записывает время автризации
    created_at =fields.DatetimeField(auto_now_add=True)
    name = fields.CharField(64)

    class Meta:
        table ='users'

UserSchema=pydantic_model_creator(User)