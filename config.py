import os
from dotenv import load_dotenv

load_dotenv()

# Bot Token
BOT_TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')

# Channel & Group Requirements
CHANNEL_USERNAME = "@your_channel"
GROUP_USERNAME = "@your_group"

# API Keys (Isi dengan API key Anda)
DEEPSEEK_API_KEY = "your_deepseek_api_key_here"
VIRTUSIM_API_KEY = "your_virtusim_api_key_here"
TELKOMSEL_API_KEY = "your_telkomsel_api_key_here"

# Payment Settings
ADMIN_IDS = [123456789]  # Ganti dengan ID admin Anda
VIP_USERS = set()

# Harga Settings
PULSA_PRICE = 1000  # per pulsa
KUOTA_PRICE = 5000  # per GB
NOKOS_PRICE = 15000
BITCOIN_PRICE = 100000
APK_PRICE = 50000
WEBSITE_PRICE = 75000

COUNTRIES = [
    "Indonesia", "USA", "UK", "Singapore", "Malaysia",
    "Japan", "Germany", "Australia", "Brazil", "India"
]