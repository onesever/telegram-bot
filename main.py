import telebot
from telebot import types
import os

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

CHANNEL_ID = "@blackrussia85"  # твой канал
ADMIN_ID = 724545647           # твой Telegram ID

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Отправь сюда объявление для публикации 📝")

@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "Ты админ, все ок ✅")
        return

    if message.photo:
        file_id = message.photo[-1].file_id
        caption = message.caption or "Без описания"
        bot.send_photo(ADMIN_ID, file_id, caption=f"🔔 Новое объявление:\n\n{caption}\n\nОдобрить /post")
    else:
        bot.send_message(ADMIN_ID, f"🔔 Новое объявление:\n\n{message.text}\n\nОдобрить /post")

@bot.message_handler(commands=['post'])
def approve(message):
    bot.send_message(message.chat.id, "✅ Объявление опубликовано!")
    # здесь бот сам постит в канал
    bot.send_message(CHANNEL_ID, "Новое объявление от пользователя!")

print("Бот запущен...")
bot.infinity_polling()
