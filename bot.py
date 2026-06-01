import telebot
import os
import requests
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Настройки из переменных Render
TOKEN = os.environ.get("TELEGRAM_TOKEN")
API_KEY = os.environ.get("AI_API_KEY")
PORT = int(os.environ.get("PORT", 8080))

bot = telebot.TeleBot(TOKEN)

# Веб-сервер на встроенной библиотеке Python (на сто процентов не требует Flask)
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.end_headers()
        self.wfile.write("Бот работает!".encode('utf-8'))

def run_server():
    server = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print(f"Встроенный веб-сервер запущен на порту {PORT}")
    server.serve_forever()

# Запускаем веб-сервер в отдельном потоке, чтобы он не мешал боту
threading.Thread(target=run_server, daemon=True).start()

# Функция запроса к Gemini
def ask_ai(text):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"
    try:
        response = requests.post(url, json={"contents": [{"parts": [{"text": text}]}]}, timeout=15)
        if response.status_code == 200:
            return response.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            return f"Ошибка API ({response.status_code})"
    except Exception as e:
        return f"Ошибка подключения: {str(e)}"

# Обработчик сообщений в Telegram
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    reply = ask_ai(message.text)
    bot.reply_to(message, reply)

print("Бот успешно запущен и слушает команды!")
bot.infinity_polling()
