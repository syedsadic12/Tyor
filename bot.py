import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio

# Environment Variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS = os.getenv('CHANNELS').split(',')  # Format: @channel1,@channel2
FINAL_CODE = os.getenv('FINAL_CODE')
BASE_URL = os.getenv('BASE_URL')  # e.g., https://your-render-url.onrender.com

# Flask App
app = Flask(__name__)

# Telegram Bot Application
application = Application.builder().token(BOT_TOKEN).build()

# Home route
@app.route('/')
def home():
    return "🤖 Bot is live and running!"

# Webhook route
@app.route(f'/{BOT_TOKEN}', methods=['POST'])
async def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    await application.process_update(update)
    return "ok"

# /start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/trygfxm")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/trygfx")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/moviezmp")],
        [InlineKeyboardButton("✅ Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "📲 Join these channels and click ✅ Verify to receive your code:",
        reply_markup=reply_markup
    )

# Verify button callback handler
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
        except:
            joined_all = False
            break

    if joined_all:
        await query.edit_message_text(
            f"✅ Verified!\nYour code: `{FINAL_CODE}`",
            parse_mode='Markdown'
        )
    else:
        await query.edit_message_text(
            "❌ You haven't joined all required channels.\nPlease join and click Verify again."
        )

def main():
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(verify))

    # Set webhook before starting the Flask server
    async def set_webhook():
        await application.bot.set_webhook(url=f"{BASE_URL}/{BOT_TOKEN}")
        print("✅ Webhook set!")

    asyncio.get_event_loop().run_until_complete(set_webhook())

    # Start Flask server
    app.run(host="0.0.0.0", port=10000)

if __name__ == '__main__':
    main()
