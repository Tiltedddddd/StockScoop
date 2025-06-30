from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import datetime
import os
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")


from news import get_news_for_ticker
from logic import analyze_news
from utils import is_valid_ticker, load_watchlist, save_watchlist


# Start command handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(update.effective_user.id)
    await update.message.reply_text(
        "👋 Welcome to StockScoop!\n\nUse the following commands:\n" 
        "/holdings [TICKERS] — Get news summaries with sentiment (e.g. /holdings NVDA, SOFI)\n"
        "/holdings --brief — Quick headlines only (uses saved tickers)\n"
        "/save [TICKERS] — Save tickers to your watchlist\n"
        "/watchlist — View your current saved tickers\n"
        "🕗 Daily updates are sent every morning at 8AM using your saved watchlist."
    )


# Holdings command handler
async def holdings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_input = " ".join(context.args)
    is_brief = "--brief" in raw_input.lower()

    # Remove --brief and parse tickers
    clean_input = raw_input.replace("--brief", "")
    tickers = [t.strip().upper() for t in clean_input.split(",") if t.strip()]

    # Fallback to watchlist if no tickers typed
    if not tickers:
        tickers = load_watchlist()

    reply = "📝 *Brief mode enabled – showing headlines only*\n\n" if is_brief else ""

    for ticker in tickers:
        if not is_valid_ticker(ticker):
            reply += f"\nInvalid Ticker: *{ticker}*\n"
            continue

        news = get_news_for_ticker(ticker)

        reply += f"\n📰 *{ticker}*\n"

        if is_brief:
            for article in news:
                reply += f"• [{article['title']}]({article.get('link', '')})\n"
        else:
            recommendation, sentiments = analyze_news(news)
            reply += "\n".join(f"• {s}" for s in sentiments)
            reply += f"\n\n💡 {recommendation}\n"

    await update.message.reply_text(reply or "No news found.", parse_mode="Markdown", disable_web_page_preview=True)


# Save command
async def save(update: Update, context: ContextTypes.DEFAULT_TYPE):
    raw_input = " ".join(context.args)
    tickers = [t.strip().upper() for t in raw_input.split(",") if t.strip()]

    valid = [t for t in tickers if is_valid_ticker(t)]

    if not valid:
        await update.message.reply_text("No valid tickers provided.")
        return

    save_watchlist(valid)
    await update.message.reply_text(f"✅ Watchlist saved: {', '.join(valid)}")


# Watchlist command
async def watchlist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    tickers = load_watchlist()
    if not tickers:
        await update.message.reply_text("No watchlist saved.")
    else:
        await update.message.reply_text(f"📊 Current watchlist: {', '.join(tickers)}")


async def send_daily_update(bot):
    user_id = 1609231367
    tickers = load_watchlist()

    if not tickers:
        return

    reply = f"🕗 *Daily StockScoop Update – {datetime.date.today()}*\n"

    for ticker in tickers:
        news = get_news_for_ticker(ticker)
        recommendation, sentiments = analyze_news(news)
        reply += f"\n📰 *{ticker}*\n"
        reply += "\n".join(f"• {s}" for s in sentiments)
        reply += f"\n\n💡 {recommendation}\n"

    try:
        await bot.send_message(chat_id=user_id, text=reply, parse_mode="Markdown", disable_web_page_preview=True)
    except Exception as e:
        print(f"[Scheduler Error] {e}")

# Run bot
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("holdings", holdings))
    app.add_handler(CommandHandler("save", save))
    app.add_handler(CommandHandler("watchlist", watchlist))

    print("Bot is running...")
    scheduler = BackgroundScheduler()

    # Run daily at 8AM
    scheduler.add_job(lambda: asyncio.run(send_daily_update(app.bot)), "cron", hour=7)# type: ignore

    scheduler.start()
    print("Scheduler started...")

    app.run_polling()

