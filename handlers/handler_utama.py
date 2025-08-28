# /opt/hokage-bot/handlers/handler_utama.py (VERSI FINAL)

import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, ConversationHandler
import keyboards, database, config
from . import states, handler_auth

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.effective_user
    user_id = user.id
    logger.info(f"User {user_id} memulai percakapan.")
    database.add_user_if_not_exists(user_id, user.first_name, user.username)

    if database.check_user_verification(user_id):
        logger.info(f"User {user_id} sudah terverifikasi. Menampilkan menu utama.")
        await update.message.reply_text("🤖 Selamat datang kembali!", reply_markup=keyboards.get_main_menu_keyboard(user_id, context))
        return states.ROUTE
    else:
        logger.info(f"User {user_id} belum terverifikasi. Memulai alur registrasi.")
        return await handler_auth.ask_for_phone_number(update, context)

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await update.effective_message.reply_text("Silakan pilih dari menu di bawah:", reply_markup=keyboards.get_main_menu_keyboard(user_id, context))
    return states.ROUTE

async def route_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (Isi fungsi ini bisa disesuaikan lagi nanti, untuk sekarang biarkan sederhana)
    query = update.callback_query
    await query.answer("Fitur ini sedang dalam pengembangan.")
    return states.ROUTE

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    await update.effective_chat.send_message("❌ Operasi dibatalkan.", reply_markup=keyboards.get_main_menu_keyboard(user_id, context))
    return ConversationHandler.END