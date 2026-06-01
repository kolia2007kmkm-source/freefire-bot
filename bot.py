import telebot
import os
import requests

# Берем токены из безопасных настроек сервиса
TOKEN = os.environ.get("TELEGRAM_TOKEN")
AI_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(TOKEN)

def ask_ai(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_KEY}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": text}]}]}, timeout=15)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Ошибка ИИ (Код: {response.status_code}). Проверь API ключ."
    except Exception as e:
        return f"Не удалось связаться с ИИ: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    reply = ask_ai(message.text)
    bot.reply_to(message, reply)

if __name__ == '__main__':
    print("Бот успешно запущен на сервере и готов к работе!")
    bot.infinity_polling()
