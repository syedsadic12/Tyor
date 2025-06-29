import os
import asyncio
import threading
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS = os.getenv('CHANNELS').split(',')
FINAL_CODE = os.getenv('FINAL_CODE')

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot is running successfully!"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/trygfxm")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/trygfx")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/moviezmp")],
        [InlineKeyboardButton("✅ Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📲 Join this group for more earning or Start earning online", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
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

async def run_bot():
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    await application.run_polling()

def start_bot():
    asyncio.run(run_bot())

if __name__ == '__main__':
    threading.Thread(target=start_bot).start()
    app.run(host="0.0.0.0", port=10000)
