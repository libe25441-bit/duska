import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN", "8804297281:AAG5s5d_-qtdvpUwGHumgzmWmQsD_wQtZGE")

ITEMS = [
    {'photo': 'https://picsum.photos/400/300?random=1', 'caption': '🌄 Горный пейзаж\nУтро в Альпах'},
    {'photo': 'https://picsum.photos/400/300?random=2', 'caption': '🏖️ Пляжный отдых\nБирюзовая вода'},
    {'photo': 'https://picsum.photos/400/300?random=3', 'caption': '🏙️ Ночной город\nОгни мегаполиса'},
    {'photo': 'https://picsum.photos/400/300?random=4', 'caption': '🌲 Лесная тропа\nХвойный лес'},
    {'photo': 'https://picsum.photos/400/300?random=5', 'caption': '🌸 Цветущий сад\nСакура весной'}
]

user_positions = {}

def get_keyboard(index, total):
    row = []
    if index > 0:
        row.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"prev_{index}"))
    row.append(InlineKeyboardButton(f"📌 {index+1}/{total}", callback_data="pos"))
    if index < total - 1:
        row.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"next_{index}"))
    return InlineKeyboardMarkup([row])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_positions[update.effective_user.id] = 0
    await show_item(update, context, 0)

async def show_item(update, context, index):
    q = update.callback_query
    user_positions[update.effective_user.id] = index
    item = ITEMS[index]
    kb = get_keyboard(index, len(ITEMS))
    if q:
        await q.edit_message_media(media=item['photo'], reply_markup=kb)
        await q.edit_message_caption(caption=item['caption'], reply_markup=kb)
    else:
        await update.message.reply_photo(photo=item['photo'], caption=item['caption'], reply_markup=kb)

async def callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data.startswith("next_"):
        idx = int(data.split("_")[1]) + 1
        if idx < len(ITEMS): await show_item(update, context, idx)
    elif data.startswith("prev_"):
        idx = int(data.split("_")[1]) - 1
        if idx >= 0: await show_item(update, context, idx)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback))
    print("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
