import telebot
import os
import requests
from flask import Flask
from threading import Thread

# Загружаем ключи из настроек Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
AI_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Веб-сервер, чтобы Render не выключал бота
@app.route('/')
def home():
    return "Бот активен"

def run_web():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

# Функция запроса к Gemini
def ask_ai(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_KEY}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": text}]}]}, timeout=15)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Ошибка API: {response.status_code}"
    except Exception as e:
        return f"Ошибка: {str(e)}"

# Главный обработчик сообщений
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Отправляем текст пользователя в ИИ и пишем ответ в логи для отладки
    reply = ask_ai(message.text)
    print(f"Пользователь: {message.text} | Бот: {reply}") 
    bot.reply_to(message, reply)

if __name__ == '__main__':
    Thread(target=run_web).start()
    bot.infinity_polling()
