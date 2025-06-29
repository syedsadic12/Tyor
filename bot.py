
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes
import os

BOT_TOKEN = os.getenv('BOT_TOKEN')
CHANNELS = os.getenv('CHANNELS').split(',')
FINAL_CODE = os.getenv('FINAL_CODE')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/trygfxm")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/trygfx")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/moviezmp")],
        [InlineKeyboardButton("✅ Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Join this group for more earning or Start earning online", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    joined_all = True

    for channel in CHANNELS:
        try:
            member = await context.bot.get_chat_member(chat_id=channel, user_id=user_id)
            if member.status not in ['member', 'administrator', 'creator']:
                joined_all = False
                break
        except Exception:
            joined_all = False
            break

    if joined_all:
        await query.edit_message_text(f"✅ Verified!\nYour code: `{FINAL_CODE}`", parse_mode='Markdown')
    else:
        await query.edit_message_text("❌ You haven't joined all required channels.\nPlease join and then click Verify.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()

if __name__ == '__main__':
    main()
