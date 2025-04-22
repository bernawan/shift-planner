from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler,
    filters, ContextTypes
)
from db import init_db, tambah_shift, get_shift_by_tanggal
import os

BOT_TOKEN = os.getenv("8004694666:AAFu8Elye4z0gnERN3tYa9f7f6t2ci8g8CE")

user_steps = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani perintah /start untuk memulai interaksi dengan bot"""
    await update.message.reply_text("Halo! Gunakan /run untuk mengisi shift.")

async def run_shift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani perintah /run untuk mengisi shift"""
    keyboard = [[InlineKeyboardButton("Pilih Tanggal", callback_data="pilih_tanggal")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Silakan pilih menu:", reply_markup=reply_markup)

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani callback dari inline keyboard"""
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id

    if query.data == "pilih_tanggal":
        user_steps[user_id] = {"step": "tanggal"}
        await query.edit_message_text("Silakan masukkan tanggal (YYYY-MM-DD):")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani input teks dari pengguna"""
    user_id = update.message.from_user.id
    text = update.message.text

    if user_id not in user_steps:
        return

    step = user_steps[user_id]["step"]

    if step == "tanggal":
        user_steps[user_id]["tanggal"] = text
        user_steps[user_id]["step"] = "pengganti"
        await update.message.reply_text("Masukkan nama pengganti:")
    elif step == "pengganti":
        tanggal = user_steps[user_id]["tanggal"]
        username = f"@{update.message.from_user.username}"
        pengganti = text
        tambah_shift(tanggal, username, pengganti)
        await update.message.reply_text(f"Tercatat: {username} > {pengganti} di {tanggal}")
        del user_steps[user_id]

async def cek_shift(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Menangani perintah /cek untuk melihat pengganti pada tanggal tertentu"""
    if context.args:
        tanggal = context.args[0]
        result = get_shift_by_tanggal(tanggal)
        if result:
            pesan = "\n".join([f"{r[0]} > {r[1]}" for r in result])
        else:
            anggota = [m.mention_html() for m in await update.effective_chat.get_administrators()]
            pesan = "Belum ada pengganti tercatat:\n" + "\n".join(anggota)
        await update.message.reply_text(pesan, parse_mode="HTML")
    else:
        await update.message.reply_text("Gunakan format: /cek YYYY-MM-DD")

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("run", run_shift))
    app.add_handler(CommandHandler("cek", cek_shift))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.run_polling()
