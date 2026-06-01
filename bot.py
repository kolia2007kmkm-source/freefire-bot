import telebot
import requests
import os

# Получаем данные из настроек сервера (Environment Variables)
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
AI_API_KEY = os.environ.get("AI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

SYSTEM_INSTRUCTION = "Ты — тренер по Free Fire. Отвечай только по настройкам чувствительности и DPI. Если спрашивают другое — отказывай."

def ask_gemini(user_text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={AI_API_KEY}"
    payload = {"contents": [{"parts": [{"text": user_text}]}]}
    try:
        response = requests.post(url, json=payload, headers={"Content-Type": "application/json"}, timeout=10)
        return response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return "Братик, ошибочка при связи с ИИ. Попробуй еще раз!"

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    response = ask_gemini(message.text)
    bot.reply_to(message, response)

if __name__ == '__main__':
    bot.infinity_polling()
