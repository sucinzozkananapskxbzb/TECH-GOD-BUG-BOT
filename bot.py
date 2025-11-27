import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN, ADMIN_IDS
from database import db
from handlers import auth, workout, trading, coding, fun, ai, payment, admin

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    if not db.check_registration(user_id):
        # Register new user
        user = update.effective_user
        db.register_user(user.id, user.username, user.first_name, user.last_name)
        
        keyboard = [
            [InlineKeyboardButton("✅ Join Channel", url="https://t.me/your_channel")],
            [InlineKeyboardButton("✅ Join Group", url="https://t.me/your_group")],
            [InlineKeyboardButton("🔄 Cek Keanggotaan", callback_data="check_membership")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "👋 **Selamat Datang!**\n\n"
            "Untuk menggunakan bot ini, Anda harus:\n"
            "1. Join channel kami\n"
            "2. Join group kami\n\n"
            "Setelah join, klik tombol 'Cek Keanggotaan'",
            reply_markup=reply_markup
        )
    else:
        if db.check_membership(user_id) or db.is_vip(user_id) or user_id in ADMIN_IDS:
            await show_main_menu(update, context)
        else:
            await update.message.reply_text("❌ Anda belum memenuhi syarat keanggotaan. Silakan join channel dan group terlebih dahulu.")

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("💪 Anak Workout", callback_data="menu_workout")],
        [InlineKeyboardButton("📈 Trading", callback_data="menu_trading")],
        [InlineKeyboardButton("💻 Coding", callback_data="menu_coding")],
        [InlineKeyboardButton("😊 Fun Menu", callback_data="menu_fun")],
        [InlineKeyboardButton("🤖 AI Tools", callback_data="menu_ai")],
        [InlineKeyboardButton("💰 Payment & Top Up", callback_data="menu_payment")],
        [InlineKeyboardButton("🌐 Terjemahan", callback_data="menu_translate")]
    ]
    
    if update.effective_user.id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data="menu_admin")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🎯 **Menu Utama Bot**\n\n"
        "Pilih kategori fitur yang ingin digunakan:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    
    # Check if user has access
    if not (db.check_membership(user_id) or db.is_vip(user_id) or user_id in ADMIN_IDS):
        await query.edit_message_text("❌ Akses ditolak. Silakan penuhi syarat keanggotaan terlebih dahulu.")
        return
    
    data = query.data
    
    if data == "check_membership":
        await auth.check_membership(query, context)
    elif data == "menu_workout":
        await workout.show_workout_menu(query, context)
    elif data == "menu_trading":
        await trading.show_trading_menu(query, context)
    elif data == "menu_coding":
        await coding.show_coding_menu(query, context)
    elif data == "menu_fun":
        await fun.show_fun_menu(query, context)
    elif data == "menu_ai":
        await ai.show_ai_menu(query, context)
    elif data == "menu_payment":
        await payment.show_payment_menu(query, context)
    elif data == "menu_admin":
        await admin.show_admin_menu(query, context)
    elif data == "menu_translate":
        await query.edit_message_text("🌐 **Fitur Terjemahan**\n\nFitur dalam pengembangan...")
    elif data == "back_to_main":
        await show_main_menu_from_query(query, context)

async def show_main_menu_from_query(query, context):
    keyboard = [
        [InlineKeyboardButton("💪 Anak Workout", callback_data="menu_workout")],
        [InlineKeyboardButton("📈 Trading", callback_data="menu_trading")],
        [InlineKeyboardButton("💻 Coding", callback_data="menu_coding")],
        [InlineKeyboardButton("😊 Fun Menu", callback_data="menu_fun")],
        [InlineKeyboardButton("🤖 AI Tools", callback_data="menu_ai")],
        [InlineKeyboardButton("💰 Payment & Top Up", callback_data="menu_payment")],
        [InlineKeyboardButton("🌐 Terjemahan", callback_data="menu_translate")]
    ]
    
    if query.from_user.id in ADMIN_IDS:
        keyboard.append([InlineKeyboardButton("👑 Admin Panel", callback_data="menu_admin")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.edit_message_text(
        "🎯 **Menu Utama Bot**\n\n"
        "Pilih kategori fitur yang ingin digunakan:",
        reply_markup=reply_markup
    )

def main():
    application = Application.builder().token(BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Admin handlers
    application.add_handler(CommandHandler("addvip", admin.add_vip))
    application.add_handler(CommandHandler("delvip", admin.del_vip))
    application.add_handler(CommandHandler("broadcast", admin.broadcast))
    
    print("Bot started...")
    application.run_polling()

if __name__ == '__main__':
    main()