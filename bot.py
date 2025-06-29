import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ✅ Load environment variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS = os.getenv('CHANNELS', '').split(',')
FINAL_CODE = os.getenv('FINAL_CODE', '00poonmoon98')
BASE_URL = os.getenv('BASE_URL', 'https://tyor-1.onrender.com')

# ✅ Debug Print
print("BOT_TOKEN:", BOT_TOKEN)
print("CHANNELS:", CHANNELS)
print("BASE_URL:", BASE_URL)

# ✅ Flask app init
app = Flask(__name__)
application = Application.builder().token(BOT_TOKEN).build()

# ✅ Flask root to confirm server is live
@app.route('/')
def home():
    return "Bot is live!"

# ✅ Webhook endpoint
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# ✅ /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"/start received from user: {update.effective_user.id}")
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/trygfxm")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/trygfx")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/moviezmp")],
        [InlineKeyboardButton("✅ Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📲 Join this group for more earning or Start earning online", 
        reply_markup=reply_markup
    )

# ✅ Verify button handler
async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    joined_all = True

    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel.strip(), user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                joined_all = False
                break
        except Exception as e:
            print(f"Error checking channel {channel}: {e}")
            joined_all = False
            break

    if joined_all:
        await query.edit_message_text(f"✅ Verified!\nYour code: `{FINAL_CODE}`", parse_mode='Markdown')
    else:
        await query.edit_message_text(
            "❌ You haven't joined all required channels.\nPlease join and click Verify again."
        )

# ✅ Start the app
def main():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(verify))

    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=f"{BASE_URL}/{BOT_TOKEN}"
    )

if __name__ == '__main__':
    main()
