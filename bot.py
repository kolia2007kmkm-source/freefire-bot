import telebot
import os
from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading

# Твой бот
bot = telebot.TeleBot(os.environ.get("TELEGRAM_TOKEN"))

# Функция-заглушка, чтобы Render видел открытый порт
def run_dummy_server():
    server = HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8080))), SimpleHTTPRequestHandler)
    server.serve_forever()

# Запускаем "заглушку" в отдельном потоке
threading.Thread(target=run_dummy_server).start()

# Запускаем бота
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    # Тут твоя логика с ИИ...
    bot.reply_to(message, "Работаю!") 

bot.infinity_polling()
