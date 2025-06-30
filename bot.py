from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import asyncio
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNELS = os.getenv("CHANNELS", "@trygfxm,@trygfx,@moviezmp").split(",")
FINAL_CODE = os.getenv("FINAL_CODE", "00poonmoon98")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/trygfxm")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/trygfx")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/moviezmp")],
        [InlineKeyboardButton("✅ Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📲 Join all channels and click Verify", reply_markup=reply_markup)

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
            print(f"Error checking {channel}: {e}")
            joined_all = False
            break

    if joined_all:
        await query.edit_message_text(f"✅ Verified!\nYour code: `{FINAL_CODE}`", parse_mode='Markdown')
    else:
        await query.edit_message_text("❌ You haven't joined all required channels.\nJoin and click Verify again.")

async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify))

    print("🤖 Bot is running with polling...")
    await app.run_polling()

if __name__ == '__main__':
    asyncio.run(main())
