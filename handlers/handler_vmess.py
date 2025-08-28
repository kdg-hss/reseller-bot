# /opt/hokage-bot/handlers/handler_vmess.py

from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# Impor modul dari luar
import keyboards

# Impor modul dari dalam package handlers
from . import states
from .handler_utils import send_script_output, handle_script_error, run_script_and_reply

# --- VMESS Creation ---
async def vmess_get_user(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['user'] = update.message.text
    await update.message.reply_text("➡️ Masukkan Durasi (hari):")
    return states.VMESS_GET_DURATION

async def vmess_get_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    if not update.message.text.isdigit() or int(update.message.text) <= 0:
        await update.message.reply_text("❌ Durasi harus berupa angka positif.")
        return states.VMESS_GET_DURATION
    
    context.user_data['duration'] = update.message.text
    ud = context.user_data
    
    await update.message.reply_text("⏳ Membuat akun VMESS...")
    await send_script_output(update, context, ['sudo', '/opt/julak-bot/create_vmess_user.sh', ud['user'], ud['duration']])
    
    context.user_data.clear()
    return states.ROUTE

# --- VMESS List & Config ---
async def vmess_list_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("⏳ Mengambil daftar akun VMESS...")

    try:
        p = await run_script_and_reply(update, context, ['sudo', '/opt/julak-bot/list_vmess_users.sh'], "Daftar Akun VMESS")
    except Exception as e:
        await handle_script_error(update, context, e)
        return states.ROUTE
        
    return states.VMESS_SELECT_ACCOUNT

async def vmess_select_account_and_show_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user_input = update.message.text
    if user_input == '0':
        await update.message.reply_text("Dibatalkan.", reply_markup=keyboards.get_main_menu_keyboard(update.effective_user.id, context))
        context.user_data.clear()
        return states.ROUTE

    await update.message.reply_text(f"⏳ Mengambil konfigurasi untuk akun nomor {user_input}...")
    await send_script_output(update, context, ['sudo', '/opt/julak-bot/get_vmess_config.sh', user_input])
    context.user_data.clear()
    return states.ROUTE

# --- VMESS Renew ---
async def renew_vmess_get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['renew_username'] = update.message.text
    await update.message.reply_text("➡️ Sekarang, masukkan durasi perpanjangan (misal: 30 untuk 30 hari).")
    return states.RENEW_VMESS_GET_DURATION

async def renew_vmess_get_duration_and_execute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    duration = update.message.text
    if not duration.isdigit() or int(duration) <= 0:
        await update.message.reply_text("❌ Durasi harus berupa angka positif.")
        return states.RENEW_VMESS_GET_DURATION

    username = context.user_data.get('renew_username')
    await update.message.reply_text("⏳ Memproses perpanjangan VMESS...")
    await send_script_output(update, context, ['sudo', '/opt/julak-bot/create_renew_vmess.sh', username, duration])
    context.user_data.clear()
    return states.ROUTE
    
# --- VMESS Trial ---
async def create_vmess_trial_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    duration = "1" # Durasi trial bisa diatur di sini
    await update.message.reply_text("⏳ Membuat akun Trial VMESS...")
    await send_script_output(update, context, ['sudo', '/opt/julak-bot/create_trial_vmess.sh', duration])
    return ConversationHandler.END
