import telebot
import requests
import os
from flask import Flask
from threading import Thread

# Настройки из переменных окружения (Render)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
AI_API_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
app = Flask(__name__)

# Веб-сервер для того, чтобы Render считал сервис активным
@app.route('/')
def home():
    return "Бот работает!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Функция запроса к Gemini с выводом ошибок в логи
def ask_gemini(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": user_text}]}]}
    
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=15)
        
        if response.status_code == 200:
            data = response.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]
        else:
            # Выводим реальную ошибку в логи Render
            print(f"ОШИБКА API ({response.status_code}): {response.text}")
            return f"Ошибочка ИИ (Код {response.status_code}). Проверь ключи в настройках."
            
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        return "Беда с подключением к серверу ИИ."

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = ask_gemini(message.text)
    bot.reply_to(message, response)

if __name__ == '__main__':
    # Запускаем веб-сервер в фоне
    Thread(target=run_web).start()
    # Запускаем бота
    bot.infinity_polling()
