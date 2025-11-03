import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "724545647"))  # Твой ID
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1002807174993"))

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# Главное меню
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("📢 Отправить объявление"))
main_menu.add(KeyboardButton("📩 Связь с админом"))
main_menu.add(KeyboardButton("ℹ️ Помощь"))

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.answer("Привет! 👋\nВыберите действие ниже 👇", reply_markup=main_menu)

@dp.message_handler(lambda message: message.text == "ℹ️ Помощь")
async def help_info(message: types.Message):
    text = (
        "📋 Пример объявления:\n"
        "1. Куплю/Продам - ...\n"
        "2. Цена - ...\n"
        "3. Связь - @вашюзер\n\n"
        "Все одним сообщением! Фото можно прикрепить 🙂"
    )
    await message.answer(text)

@dp.message_handler(lambda message: message.text == "📩 Связь с админом")
async def contact_admin(message: types.Message):
    await message.answer("Связаться с админом: @onesever")

@dp.message_handler(lambda message: message.text == "📢 Отправить объявление")
async def send_ad(message: types.Message):
    await message.answer("✍️ Отправьте текст объявления (и фото, если нужно) одним сообщением.")

@dp.message_handler(content_types=["text", "photo"])
async def handle_submission(message: types.Message):
    if message.text in ["📢 Отправить объявление", "📩 Связь с админом", "ℹ️ Помощь"]:
        return

    approve_kb = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✅ Одобрить", callback_data="approve"),
        InlineKeyboardButton("❌ Отклонить", callback_data="reject")
    )

    caption = f"Новое объявление от @{message.from_user.username or 'пользователя'}"
    if message.photo:
        await message.photo[-1].send_to_chat(ADMIN_ID, caption=caption)
    else:
        await bot.send_message(ADMIN_ID, f"{caption}\n\n{message.text}", reply_markup=approve_kb)

    await message.answer("✅ Объявление отправлено на проверку админу!")

@dp.callback_query_handler(lambda c: c.data in ["approve", "reject"])
async def handle_decision(callback_query: types.CallbackQuery):
    message = callback_query.message
    if callback_query.data == "approve":
        await bot.send_message(CHANNEL_ID, message.text)
        await bot.answer_callback_query(callback_query.id, "✅ Объявление опубликовано!")
    else:
        await bot.answer_callback_query(callback_query.id, "❌ Объявление отклонено.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
