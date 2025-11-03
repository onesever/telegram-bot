import os
import telebot

# Берём токен из переменной окружения
TOKEN = os.getenv("TOKEN")

if not TOKEN:
    raise ValueError("❌ Ошибка: переменная TOKEN не найдена. Проверь настройки Render!")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "✅ Бот успешно запущен на Render!")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запускаем бота
if __name__ == "__main__":
    print("🚀 Бот запущен и работает...")
    bot.infinity_polling()
