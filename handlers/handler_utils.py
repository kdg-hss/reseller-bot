# handlers/handler_utils.py
import logging
import subprocess
import keyboards
import database
import requests
import config
from telegram import Update
from telegram.ext import ContextTypes

# Impor dari file lain di dalam package 'handlers'

from .states import ROUTE

logger = logging.getLogger(__name__)

async def handle_script_error(update: Update, context: ContextTypes.DEFAULT_TYPE, error: Exception):
    msg = f"An unexpected error occurred: {error}"
    if isinstance(error, subprocess.CalledProcessError):
        error_output = error.stdout.strip() or error.stderr.strip()
        msg = error_output or "Script failed with a non-zero exit code but no error output."
    elif isinstance(error, FileNotFoundError):
        msg = f"Script file not found ({error}). Please check the path and permissions."
    elif isinstance(error, TimeoutError):
        msg = "Script execution timed out. It took too long to respond."

    text_to_send = f"❌ Operation Failed\n\nReason:\n{msg}"

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text_to_send,
        reply_markup=keyboards.get_back_to_menu_keyboard()
    )
    logger.error(f"Script execution error: {msg}", exc_info=True)
    return ROUTE

async def run_script_and_reply(update: Update, context: ContextTypes.DEFAULT_TYPE, script_command: list, success_message: str):
    target_message = update.callback_query.message if update.callback_query else update.message
    processing_text = "⏳ Sedang memproses, mohon tunggu..."

    if update.callback_query and target_message.text:
        try:
            await target_message.edit_text(processing_text)
        except Exception:
            await update.effective_chat.send_message(processing_text)
    else:
        await target_message.reply_text(processing_text)

    try:
        p = subprocess.run(script_command, capture_output=True, text=True, check=True, timeout=60)
        output = p.stdout.strip()
        response_text = f"✅ {success_message}\n\n{output}" if output else f"✅ {success_message}\n\nOperasi selesai."
        
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=response_text,
            reply_markup=keyboards.get_back_to_menu_keyboard()
        )
        if update.callback_query:
            await target_message.delete()
    except Exception as e:
        await handle_script_error(update, context, e)

async def send_script_output(update: Update, context: ContextTypes.DEFAULT_TYPE, script_command: list):
    try:
        p = subprocess.run(script_command, capture_output=True, text=True, check=True, timeout=30)
        await update.message.reply_text(p.stdout.strip(), reply_markup=keyboards.get_back_to_menu_keyboard())
    except Exception as e:
        await handle_script_error(update, context, e)

def request_kmsp_otp(phone_number: str) -> str | None:
    """Meminta OTP dari KMSP. Mengembalikan auth_id jika sukses, None jika gagal."""
    try:
        url = f"https://golang-openapi-reqotp-xltembakservice.kmsp-store.com/v1?api_key={config.KMSP_API_KEY}&phone={phone_number}&method=OTP"
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        result = response.json()
        
        auth_id = result.get('data', {}).get('auth_id')
        if not auth_id:
            logger.error(f"KMSP req OTP gagal: {result.get('message', 'auth_id tidak ditemukan')}")
            return None
            
        logger.info(f"KMSP req OTP sukses untuk {phone_number}, auth_id: {auth_id}")
        return auth_id
    except Exception as e:
        logger.error(f"Exception di request_kmsp_otp: {e}")
        return None

def verify_kmsp_otp(phone_number: str, auth_id: str, otp_code: str) -> str | None:
    """Memverifikasi OTP ke KMSP. Mengembalikan access_token jika sukses, None jika gagal."""
    try:
        url = f"https://golang-openapi-login-xltembakservice.kmsp-store.com/v1?api_key={config.KMSP_API_KEY}&phone={phone_number}&method=OTP&auth_id={auth_id}&otp={otp_code}"
        response = requests.get(url, timeout=20)
        response.raise_for_status()
        result = response.json()

        access_token = result.get('data', {}).get('access_token')
        if not access_token:
            logger.error(f"KMSP verify OTP gagal: {result.get('message', 'access_token tidak ditemukan')}")
            return None
        
        logger.info(f"KMSP verify OTP sukses untuk {phone_number}")
        return access_token
    except Exception as e:
        logger.error(f"Exception di verify_kmsp_otp: {e}")
        return None
