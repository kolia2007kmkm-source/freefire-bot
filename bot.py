import telebot
import os
import requests
import time

TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(TOKEN)

def ask_ai(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": text}]}]}, timeout=15)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Ошибка API: {response.status_code}"
    except Exception as e:
        return f"Ошибка подключения: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    reply = ask_ai(message.text)
    bot.reply_to(message, reply)

print("Бот запущен и ждет сообщений!")
bot.infinity_polling()
