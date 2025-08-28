# /opt/hokage-bot/main.py (VERSI FINAL & BERSIH)

import logging
from telegram.ext import (
    Application, ConversationHandler, CommandHandler, 
    CallbackQueryHandler, MessageHandler, filters, ContextTypes
)

import config
import database
from handlers import (
    states, handler_utama, handler_ssh, handler_vmess, 
    handler_vless, handler_trojan, handler_tools, handler_auth
)

# Konfigurasi logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

# Error handler untuk menangkap kesalahan tak terduga
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(msg="Exception while handling an update:", exc_info=context.error)

def main() -> None:
    """Memulai dan menjalankan bot."""
    database.init_db()
    
    application = Application.builder().token(config.BOT_TOKEN).build()
    application.add_error_handler(error_handler)
    
    # SATU ConversationHandler untuk mengatur SEMUA alur bot
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler("start", handler_utama.start)
        ],
        states={
            # State saat berada di menu utama, menunggu tombol inline ditekan
            states.ROUTE: [
                CallbackQueryHandler(handler_utama.route_handler)
            ],
            
            # State untuk alur otentikasi
            states.GET_PHONE_NUMBER: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler_auth.phone_number_received)
            ],
            states.GET_KMSP_OTP: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler_auth.kmsp_otp_received)
            ],
            
            # State untuk alur pembuatan akun SSH
            states.SSH_GET_USERNAME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler_ssh.ssh_get_username)
            ],
            states.SSH_GET_PASSWORD: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler_ssh.ssh_get_password)
            ],
            states.SSH_GET_DURATION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handler_ssh.ssh_get_duration)
            ],
            # ... (Tambahkan state lain dari modul handler Anda di sini jika ada)
        },
        fallbacks=[
            CommandHandler("start", handler_utama.start),
            CommandHandler("menu", handler_utama.menu),
            CommandHandler("cancel", handler_utama.cancel),
        ],
        per_user=True,
        per_chat=True,
    )

    # Hanya daftarkan satu handler utama ini
    application.add_handler(conv_handler)

    logger.info("Bot started and running...")
    application.run_polling()

if __name__ == "__main__":
    main()