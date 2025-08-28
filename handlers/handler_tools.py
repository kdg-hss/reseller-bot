# handlers/handler_tools.py
import os
import re
import subprocess
import keyboards
import database
import config
from telegram import Update
from telegram.ext import ContextTypes

# Impor dari file lain di dalam package 'handlers'
from .states import *
from .handler_utils import run_script_and_reply, handle_script_error

# --- Backup ---
async def handle_backup(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (salin seluruh kode fungsi handle_backup ke sini) ...
    return ROUTE

# --- Delete ---
async def delete_get_username(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (salin seluruh kode fungsi delete_get_username ke sini) ...
    return DELETE_CONFIRMATION

async def delete_confirmation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # ... (salin seluruh kode fungsi delete_confirmation ke sini) ...
    return ROUTE
