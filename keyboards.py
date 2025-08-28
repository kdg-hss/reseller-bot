import config
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes

def get_main_menu_keyboard(user_id: int, context: ContextTypes.DEFAULT_TYPE) -> InlineKeyboardMarkup:
    """
    Menghasilkan keyboard menu utama yang dinamis.
    Menampilkan tombol admin hanya jika pengguna adalah admin dan dalam mode admin.
    """
    # Tombol standar yang dilihat semua pengguna
    keyboard = [
        [
            InlineKeyboardButton("💰 Cek Saldo", callback_data="check_balance"),
            InlineKeyboardButton("➕ Top Up", callback_data="top_up_balance")
        ],
        [InlineKeyboardButton("🌐 SSH/VPN", callback_data="menu_ssh")],
        [InlineKeyboardButton("🚀 VMESS", callback_data="menu_vmess")],
        [InlineKeyboardButton("⚡ VLESS", callback_data="menu_vless")],
        [InlineKeyboardButton("🐴 TROJAN", callback_data="menu_trojan")],
    ]

    is_admin = user_id in config.ADMIN_IDS
    
    if is_admin:
        # Dapatkan mode tampilan saat ini dari context, defaultnya 'admin'
        view_mode = context.user_data.get('view_mode', 'admin')

        if view_mode == 'admin':
            # Jika admin dalam mode admin, tampilkan tombol Tools dan tombol switch ke user
            keyboard.append([InlineKeyboardButton("🔧 Server Tools", callback_data="menu_tools")])
            keyboard.append([InlineKeyboardButton("🕶️ Tampilan User", callback_data="switch_to_user_view")])
        else: # view_mode == 'user'
            # Jika admin dalam mode user, sembunyikan tombol Tools dan tampilkan tombol kembali ke admin
            keyboard.append([InlineKeyboardButton("👑 Kembali ke Admin", callback_data="switch_to_admin_view")])
    
    # Tombol tutup menu untuk semua
    keyboard.append([InlineKeyboardButton("❌ Tutup Menu", callback_data="close_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def get_ssh_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("➕ Buat Akun Baru", callback_data="ssh_add")],
        [InlineKeyboardButton("🔄 Perpanjang Akun", callback_data="ssh_renew")],
        [InlineKeyboardButton("🎁 Akun Trial", callback_data="ssh_trial")],
        [InlineKeyboardButton("🗑️ Hapus Akun", callback_data="ssh_delete")],
        # Tombol yang sudah ada untuk List Akun (akan jadi interaktif)
        [InlineKeyboardButton("📋 List Akun", callback_data="ssh_list")], 
        # Tombol baru untuk Config User (akan mengarah ke alur list interaktif)
        [InlineKeyboardButton("🔍 Config User", callback_data="ssh_config_user")], # <--- TOMBOL BARU
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_vmess_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("➕ Buat Akun Baru", callback_data="vmess_add")],
        [InlineKeyboardButton("🎁 Akun Trial", callback_data="vmess_trial")],
        [InlineKeyboardButton("🗑️ Hapus Akun", callback_data="vmess_delete")],
        [InlineKeyboardButton("📋 List Akun", callback_data="vmess_list")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_vless_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("➕ Buat Akun Baru", callback_data="vless_add")],
        [InlineKeyboardButton("🎁 Akun Trial", callback_data="vless_trial")],
        [InlineKeyboardButton("🗑️ Hapus Akun", callback_data="vless_delete")],
        [InlineKeyboardButton("📋 List Akun", callback_data="vless_list")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_trojan_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("➕ Buat Akun Baru", callback_data="trojan_add")],
        [InlineKeyboardButton("🎁 Akun Trial", callback_data="trojan_trial")],
        [InlineKeyboardButton("🗑️ Hapus Akun", callback_data="trojan_delete")],
        [InlineKeyboardButton("📋 List Akun", callback_data="trojan_list")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_tools_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🟢 Cek Status", callback_data="menu_running")],
        [InlineKeyboardButton("🔄 Restart Layanan", callback_data="menu_restart")],
        [InlineKeyboardButton("☁️ Backup", callback_data="menu_backup")],
        [InlineKeyboardButton("⬇️ Restore", callback_data="confirm_restore")],
        [InlineKeyboardButton("🗑️ Trial Cleanup", callback_data="trial_cleanup")],
        [InlineKeyboardButton("🔄 Reboot Server", callback_data="reboot_server")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_renew_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("🔐 Renew SSH", callback_data="renew_ssh")],
        [InlineKeyboardButton("🔒 Renew VPN", callback_data="renew_vpn")],
        [InlineKeyboardButton("🔄 Renew All", callback_data="renew_all")],
        [InlineKeyboardButton("⬅️ Kembali", callback_data="menu_ssh")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_back_to_menu_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("⬅️ Kembali ke Menu", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("✅ Ya, Lanjutkan", callback_data="confirm_proceed")],
        [InlineKeyboardButton("❌ Batal", callback_data="cancel_action")]
    ]
    return InlineKeyboardMarkup(keyboard)
