# run_mini_app.py
from miniapp import app

if __name__ == '__main__':
    print("🚀 Запуск мини-приложения...")
    print("📱 Mini App доступен по адресу: http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)