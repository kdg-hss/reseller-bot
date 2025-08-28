# /opt/julak-bot/config.py (Pastikan isinya seperti ini di GitHub Anda)

import os
import logging

def get_admin_ids():
    admin_ids_str = os.getenv("ADMIN_IDS", "")
    if not admin_ids_str:
        logging.warning("ADMIN_IDS tidak diatur di environment.")
        return set()
    try:
        return {int(admin_id.strip()) for admin_id in admin_ids_str.split(',')}
    except ValueError:
        logging.error("Format ADMIN_IDS salah. Harap gunakan angka yang dipisah koma.")
        return set()

# Membaca variabel dari file .env yang dimuat oleh systemd
BOT_TOKEN = os.getenv("BOT_TOKEN")
KMSP_API_KEY = os.getenv("KMSP_API_KEY") # Tetap membaca dari environment
ADMIN_IDS = get_admin_ids()

# Pengecekan saat startup
if not BOT_TOKEN:
    logging.critical("FATAL ERROR: BOT_TOKEN tidak ditemukan di environment.")
if not ADMIN_IDS:
    logging.warning("PERINGATAN: Tidak ada ADMIN_IDS yang dikonfigurasi.")
