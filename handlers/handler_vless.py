# /opt/hokage-bot/handlers/handler_vless.py

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# Impor modul dari luar
import keyboards

# Impor modul dari dalam package handlers
from . import states
from .handler_utils import send_script_output, handle_script_error, run_script_and_reply

# --- VLESS Creation ---
async def vless_get_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['user'] = update.message.text
    await update.message.reply_text("➡️ Masukkan durasi akun VLESS (hari):")
    return states.VLESS_GET_DURATION

async def vless_get_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.text.isdigit() or int(update.message.text) <= 0:
        await update.message.reply_text("❌ Durasi harus berupa angka positif.")
        return states.VLESS_GET_DURATION
    context.user_data['duration'] = update.message.text
    await update.message.reply_text("➡️ Masukkan batas IP untuk akun VLESS:")
    return states.VLESS_GET_IP_LIMIT

async def vless_get_ip_limit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.text.isdigit() or int(update.message.text) < 1:
        await update.message.reply_text("❌ Batas IP harus berupa angka positif.")
        return states.VLESS_GET_IP_LIMIT
    context.user_data['ip_limit'] = update.message.text
    await update.message.reply_text("➡️ Masukkan kuota GB untuk akun VLESS (0 untuk unlimited):")
    return states.VLESS_GET_QUOTA

async def vless_get_quota_and_create(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.text.isdigit() or int(update.message.text) < 0:
        await update.message.reply_text("❌ Kuota GB harus berupa angka.")
        return states.VLESS_GET_QUOTA
    context.user_data['quota_gb'] = update.message.text
    
    await update.message.reply_text("⏳ Membuat akun VLESS...")
    ud = context.user_data
    await send_script_output(update, context, ['sudo', '/opt/julak-bot/create_vless_user.sh', ud['user'], ud['duration'], ud['ip_limit'], ud['quota_gb']])
    
    context.user_data.clear()
    return states.ROUTE

# --- VLESS List ---
async def vless_list_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await run_script_and_reply(update, context, ['sudo', '/opt/julak-bot/list_vless_users.sh'], "Daftar Akun VLESS")
    return states.ROUTE

# --- VLESS Trial ---
async def create_vless_trial_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    duration = "1" # Durasi trial bisa diatur di sini
    await update.message.reply_text("⏳ Membuat akun Trial VLESS...")
    await send_script_output(update, context, ['sudo', '/opt/julak-bot/create_trial_vless.sh', duration])
    return ConversationHandler.END
