
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import requests

BOT_TOKEN = "8143359794:AAGpRTqul5UVe_-DVjv9n1XpcMJkDsYnsHE"
TMDB_API_KEY = "520027c239fb87088834641eb0f9d770"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Welcome! Send me any movie name to get details.")

async def movie_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text
    url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={query}"
    response = requests.get(url).json()

    if response['results']:
        movie = response['results'][0]
        title = movie['title']
        overview = movie['overview']
        rating = movie['vote_average']
        poster = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
        msg = f"*{title}*
⭐ *Rating:* {rating}/10

📝 {overview}"
        await update.message.reply_photo(photo=poster, caption=msg, parse_mode='Markdown')
    else:
        await update.message.reply_text("❌ Movie not found.")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, movie_info))
app.run_polling()
