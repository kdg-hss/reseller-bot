# /opt/julak-bot/handlers/handler_auth.py (VERSI TES DENGAN INPUT TEKS)

import random
import logging
import re
from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes, ConversationHandler

import keyboards
import database
from . import states
from . import handler_utils

logger = logging.getLogger(__name__)

async def ask_for_phone_number(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Meminta pengguna untuk MENGETIK nomor telepon."""
    message = update.message or (update.callback_query and update.callback_query.message)
    
    await message.reply_text(
        "👋 Selamat Datang!\n\n"
        "Untuk melanjutkan, silakan **KETIK** nomor telepon Anda (format: 08xxxxxxxxxx).",
        reply_markup=ReplyKeyboardRemove()
    )
    return states.GET_PHONE_NUMBER

async def phone_number_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    logger.info("--- MEMASUKI FUNGSI phone_number_received (Mode Teks) ---")
    user_id = update.effective_user.id
    phone_number = update.message.text.strip()
    
    # Validasi sederhana
    if not re.match(r'^(08|62)\d{8,12}$', phone_number):
        await update.message.reply_text("❌ Format nomor telepon tidak valid. Silakan coba lagi (contoh: 081234567890).")
        return states.GET_PHONE_NUMBER # Minta lagi

    logger.info(f"Menerima nomor telepon via teks dari user {user_id}: {phone_number}")

    if phone_number.startswith('0'):
        phone_number = '62' + phone_number[1:]
    
    context.user_data['phone_number'] = phone_number
    await update.message.reply_text("⏳ Meminta kode OTP, mohon tunggu...")
    
    auth_id = handler_utils.request_kmsp_otp(phone_number)
    
    if auth_id:
        database.save_provider_auth(user_id, phone_number, 'kmsp', auth_id=auth_id)
        await update.message.reply_text("✅ Kode OTP telah dikirim. Silakan masukkan 6 digit kode OTP.")
        return states.GET_KMSP_OTP
    else:
        await update.message.reply_text("❌ Gagal meminta OTP dari server. Coba lagi atau hubungi admin.")
        return ConversationHandler.END

# Fungsi kmsp_otp_received tetap sama
async def kmsp_otp_received(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_id = update.effective_user.id
    phone_number = context.user_data.get('phone_number')
    otp_code = update.message.text.strip()
    
    auth_data = database.get_provider_auth(user_id, phone_number, 'kmsp')
    auth_id = auth_data.get('auth_id')

    if not phone_number or not auth_id:
        await update.message.reply_text("Sesi tidak valid. Silakan ulangi dari /start.")
        return ConversationHandler.END

    await update.message.reply_text("🔍 Memverifikasi kode OTP...")
    
    access_token = handler_utils.verify_kmsp_otp(phone_number, auth_id, otp_code)
    
    if access_token:
        database.save_provider_auth(user_id, phone_number, 'kmsp', access_token=access_token)
        database.set_user_phone_number(user_id, phone_number)
        database.set_user_verified(user_id)
        
        await update.message.reply_text(
            "✅ Verifikasi berhasil! Akun Anda telah terhubung.",
            reply_markup=keyboards.get_main_menu_keyboard(user_id, context)
        )
        return states.ROUTE
    else:
        await update.message.reply_text("❌ Kode OTP salah atau kedaluwarsa. Silakan coba lagi.")
        return states.GET_KMSP_OTP