# handlers/handler_ssh.py
import keyboards
import database
import config
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler

# Impor dari file lain di dalam package 'handlers'

from .states import *
from .handler_utils import send_script_output, handle_script_error

# --- SSH Creation ---
async def ssh_get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['username'] = update.message.text
    await update.message.reply_text("➡️ Masukkan Password:")
    return SSH_GET_PASSWORD

async def ssh_get_password(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    context.user_data['password'] = update.message.text
    await update.message.reply_text("➡️ Masukkan Durasi (hari):")
    return SSH_GET_DURATION

async def ssh_get_duration(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (kode fungsi ssh_get_duration) ...
    context.user_data['duration'] = update.message.text
    await update.message.reply_text("➡️ Masukkan Limit IP:")
    return SSH_GET_IP_LIMIT

async def ssh_get_ip_limit_and_create(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (kode fungsi ssh_get_ip_limit_and_create) ...
    ud = context.user_data
    await send_script_output(update, context, ['sudo', '/opt/hokage-bot/create_ssh.sh', ud['username'], ud['password'], ud['duration'], ud['ip_limit']])
    context.user_data.clear()
    return ROUTE

# --- SSH Renew ---
async def renew_ssh_get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (kode fungsi renew_ssh_get_username) ...
    return RENEW_SSH_GET_DURATION

async def renew_ssh_get_duration_and_execute(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (kode fungsi renew_ssh_get_duration_and_execute) ...
    return ROUTE

# --- SSH List ---
async def ssh_list_accounts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (kode fungsi ssh_list_accounts) ...
    return SSH_SELECT_ACCOUNT

async def ssh_select_account_and_show_config(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (kode fungsi ssh_select_account_and_show_config) ...
    return ROUTE

# --- SSH Trial ---
async def create_ssh_trial_account(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (kode fungsi create_ssh_trial_account) ...
    return ConversationHandler.END
