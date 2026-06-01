import telebot
import os
import requests
from flask import Flask
from threading import Thread

# Настройки
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Веб-сервер для Render
@app.route('/')
def home():
    return "Бот работает!"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Функция обращения к Gemini
def ask_gemini(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    payload = {"contents": [{"parts": [{"text": text}]}]}
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Ошибка API ({response.status_code}). Проверь ключ."
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Бот берет текст сообщения (message.text) и отправляет его в Gemini
    reply = ask_gemini(message.text)
    bot.reply_to(message, reply)

if __name__ == '__main__':
    Thread(target=run_web).start()
    bot.infinity_polling()
