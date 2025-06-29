import os
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Env variables
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS = os.getenv('CHANNELS').split(',')
FINAL_CODE = os.getenv('FINAL_CODE')
BASE_URL = os.getenv('BASE_URL')

# Flask app
app = Flask(__name__)

# Telegram bot app
application = Application.builder().token(BOT_TOKEN).build()

# Flask test route
@app.route('/')
def home():
    return "✅ Bot is live on Render!"

# Telegram webhook endpoint
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
    await update.message.reply_text("📲 Join all groups then click Verify to get your code.", reply_markup=reply_markup)

# Verify button handler
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
        await query.edit_message_text(f"✅ Verified!\nYour code: `{FINAL_CODE}`", parse_mode='Markdown')
    else:
        await query.edit_message_text("❌ You haven't joined all required channels.\nPlease join and click Verify again.")

# Main run logic
def main():
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(verify))

    # Webhook start
    application.run_webhook(
        listen="0.0.0.0",
        port=10000,
        webhook_url=f"{BASE_URL}/{BOT_TOKEN}"
    )

if __name__ == '__main__':
    main()
