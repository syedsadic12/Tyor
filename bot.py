from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
import nest_asyncio
import asyncio
import os

# Configs
BOT_TOKEN = "7754895064:AAGStX_lle4NsaTGej9udtX1msRsaC99I8U"
CHANNELS = ["@trygfxm", "@trygfx", "@moviezmp"]
FINAL_CODE = "00poonmoon98"

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📢 Join Channel 1", url="https://t.me/trygfxm")],
        [InlineKeyboardButton("📢 Join Channel 2", url="https://t.me/trygfx")],
        [InlineKeyboardButton("📢 Join Channel 3", url="https://t.me/moviezmp")],
        [InlineKeyboardButton("✅ Verify", callback_data='verify')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("📲 Join all channels and click Verify", reply_markup=reply_markup)

# Verification
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

# Run bot
async def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify))
    print("🤖 Bot is running...")
    await app.run_polling()

# Start event loop
if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.get_event_loop().run_until_complete(main())
