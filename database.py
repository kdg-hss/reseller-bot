# /opt/hokage-bot/database.py

import sqlite3
import logging
import datetime
import subprocess

logger = logging.getLogger(__name__)

# Tentukan path ke file database Anda
DB_PATH = 'bot_database.db'

def get_db_connection():
    """Membuat koneksi ke database dan mengembalikan objek koneksi."""
    conn = sqlite3.connect(DB_PATH)
    # Ini memungkinkan kita mengakses kolom berdasarkan nama, contoh: row['user_id']
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    Inisialisasi database SQLite.
    Membuat tabel 'users' jika belum ada dengan skema yang sudah disesuaikan.
    """
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Skema tabel users yang sudah dilengkapi untuk fitur login, saldo, dll.
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                first_name TEXT,
                username TEXT,
                phone_number TEXT UNIQUE,
                is_verified INTEGER DEFAULT 0,
                balance INTEGER DEFAULT 0,
                join_date TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS provider_credentials (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                phone_number TEXT NOT NULL,
                provider TEXT NOT NULL,
                auth_id TEXT,
                access_token TEXT,
                last_updated TEXT,
                UNIQUE(user_id, phone_number, provider)
            )
        ''')
        conn.commit()
        conn.close()
        logger.info("Database SQLite berhasil diinisialisasi dan tabel 'users' siap.")
    except Exception as e:
        logger.error(f"Gagal inisialisasi database: {e}", exc_info=True)

# --- Fungsi Manajemen User ---

def add_user_if_not_exists(user_id: int, first_name: str, username: str = None):
    """Menambahkan user ke database SQLite jika belum ada."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT user_id FROM users WHERE user_id = ?", (user_id,))
    
    if cursor.fetchone() is None:
        join_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO users (user_id, first_name, username, join_date) VALUES (?, ?, ?, ?)",
            (user_id, first_name, username, join_date)
        )
        conn.commit()
        logger.info(f"User baru {user_id} ({username}) telah ditambahkan ke database.")
    else:
        logger.debug(f"User {user_id} ({username}) sudah ada di database.")
        
    conn.close()

# --- Fungsi untuk Otentikasi (LOGIN & OTP) ---

def set_user_phone_number(user_id: int, phone_number: str) -> bool:
    """
    Menyimpan nomor telepon pengguna.
    Mengembalikan True jika berhasil, False jika nomor sudah terdaftar oleh user lain.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Cek apakah nomor telepon sudah digunakan oleh user ID yang berbeda
    cursor.execute(
        "SELECT user_id FROM users WHERE phone_number = ? AND user_id != ?",
        (phone_number, user_id)
    )
    existing_user = cursor.fetchone()
    
    if existing_user:
        # Nomor sudah terdaftar oleh orang lain
        logger.warning(f"User {user_id} mencoba mendaftarkan nomor {phone_number} yang sudah dimiliki oleh user {existing_user['user_id']}.")
        conn.close()
        return False
    else:
        # Nomor belum terdaftar atau milik user ini sendiri, lanjutkan update
        cursor.execute(
            "UPDATE users SET phone_number = ?, is_verified = 0 WHERE user_id = ?",
            (phone_number, user_id)
        )
        conn.commit()
        logger.info(f"Nomor telepon untuk user {user_id} telah diatur ke {phone_number}.")
        conn.close()
        return True
def set_user_verified(user_id: int):
    """Menandai pengguna sebagai terverifikasi (is_verified = 1)."""
    conn = get_db_connection()
    conn.execute("UPDATE users SET is_verified = 1 WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    logger.info(f"User {user_id} telah diverifikasi.")

def check_user_verification(user_id: int) -> bool:
    """Mengecek apakah pengguna sudah terverifikasi. Mengembalikan True atau False."""
    conn = get_db_connection()
    user = conn.execute("SELECT is_verified FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    
    if user and user['is_verified'] == 1:
        return True
    return False

# --- Fungsi untuk Manajemen Saldo (siap untuk digunakan nanti) ---

def get_user_balance(user_id: int) -> int:
    """Mengambil saldo pengguna dari database."""
    conn = get_db_connection()
    user = conn.execute("SELECT balance FROM users WHERE user_id = ?", (user_id,)).fetchone()
    conn.close()
    return user['balance'] if user else 0

def update_user_balance(user_id: int, new_balance: int):
    """Memperbarui saldo pengguna di database."""
    conn = get_db_connection()
    conn.execute("UPDATE users SET balance = ? WHERE user_id = ?", (new_balance, user_id))
    conn.commit()
    conn.close()
    logger.info(f"Saldo user {user_id} diperbarui menjadi {new_balance}.")


# --- Fungsi yang Memanggil Script Shell (TIDAK BERUBAH) ---
# Fungsi-fungsi ini tetap sama karena mereka berinteraksi dengan sistem, bukan database user.

async def get_ssh_account_list(user_id: int) -> str:
    """Mengambil daftar akun SSH dari sistem/VPS nyata dengan memanggil script shell."""
    logger.info(f"Fetching SSH account list from system for user: {user_id}")
    try:
        p = subprocess.run(['sudo', '/opt/julak-bot/list_ssh_users.sh'], capture_output=True, text=True, check=True, timeout=30)
        output_lines = p.stdout.strip()
        return output_lines if output_lines else "Belum ada akun SSH yang terdaftar di VPS."
    except Exception as e:
        logger.error(f"Error getting SSH account list: {e}", exc_info=True)
        return "❌ Terjadi kesalahan saat mengambil daftar akun."

async def get_vmess_account_list(user_id: int) -> str:
    """Mengambil daftar akun VMESS dari sistem/VPS nyata dengan memanggil script shell."""
    logger.info(f"Fetching VMESS account list from system for user: {user_id}")
    try:
        p = subprocess.run(['sudo', '/opt/julak-bot/list_vmess_users.sh'], capture_output=True, text=True, check=True, timeout=30)
        output_lines = p.stdout.strip()
        return output_lines if output_lines else "Belum ada akun VMESS yang terdaftar di VPS."
    except Exception as e:
        logger.error(f"Error getting VMESS account list: {e}", exc_info=True)
        return "❌ Terjadi kesalahan saat mengambil daftar akun VMESS."
        
def save_provider_auth(user_id: int, phone: str, provider: str, auth_id: str = None, access_token: str = None):
    """Menyimpan atau memperbarui auth_id dan access_token untuk provider tertentu."""
    conn = get_db_connection()
    now = datetime.datetime.now().isoformat()
    
    # Cek apakah sudah ada
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id FROM provider_credentials WHERE user_id = ? AND phone_number = ? AND provider = ?",
        (user_id, phone, provider)
    )
    entry = cursor.fetchone()
    
    if entry:
        # Update yang sudah ada
        if auth_id and access_token:
            cursor.execute("UPDATE provider_credentials SET auth_id = ?, access_token = ?, last_updated = ? WHERE id = ?", (auth_id, access_token, now, entry['id']))
        elif auth_id:
            cursor.execute("UPDATE provider_credentials SET auth_id = ?, last_updated = ? WHERE id = ?", (auth_id, now, entry['id']))
        elif access_token:
            cursor.execute("UPDATE provider_credentials SET access_token = ?, last_updated = ? WHERE id = ?", (access_token, now, entry['id']))
    else:
        # Buat baru
        cursor.execute(
            "INSERT INTO provider_credentials (user_id, phone_number, provider, auth_id, access_token, last_updated) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, phone, provider, auth_id, access_token, now)
        )
    conn.commit()
    conn.close()

def get_provider_auth(user_id: int, phone: str, provider: str) -> dict:
    """Mengambil data otentikasi (auth_id, access_token) untuk provider tertentu."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT auth_id, access_token FROM provider_credentials WHERE user_id = ? AND phone_number = ? AND provider = ?",
        (user_id, phone, provider)
    )
    result = cursor.fetchone()
    conn.close()
    if result:
        return {'auth_id': result['auth_id'], 'access_token': result['access_token']}
    return {}