import requests
import json


def test_openrouter_token(api_key):
    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
      "Authorization": f"Bearer {api_key}",
      "Content-Type": "application/json"
    }

    # Данные для тестового запроса (аналогично вашему примеру)
    data = {
      "model": "prime-intellect/intellect-3",  # Используем популярную модель
      "messages": [
        {
          "role": "user",
          "content": "Ответь просто 'Тест пройден!'"
        }
      ],
      "max_tokens": 10
    }

    try:
          # Исправлено: используем POST вместо GET
          response = requests.post(url, headers=headers, json=data)

          if response.status_code == 200:
              print("✅ Токен рабочий!")
              result = response.json()
              message = result['choices'][0]['message']['content']
              print(f"Ответ модели: {message}")
              return True
          else:
              print(f"❌ Ошибка: {response.status_code} - {response.text}")
              return False

    except Exception as e:
          print(f"❌ Ошибка подключения: {e}")
          return False


# Использование
api_key = 'sk-or-v1-f3ccfb91fd625346fc1c0765584185a7201555ab4a5d0117b4deaa24de86978bS'
test_openrouter_token(api_key)
