from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from config import TELEGRAM_BOT_TOKEN

# Start command handler


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to StockScoop!\nSend /holdings followed by your tickers (e.g. /holdings NVDA, SOFI)"
    )

# Holdings command handler


async def holdings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tickers = " ".join(context.args).upper().replace(" ", "").split(",")
    await update.message.reply_text(f"🔍 Tickers received: {', '.join(tickers)}\n(News coming soon...)")

# Run bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("holdings", holdings))
    print("🤖 Bot is running...")
    app.run_polling()

