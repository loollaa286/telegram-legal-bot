import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from telegram.constants import ParseMode
from app.config import BOT_TOKEN, API_URL

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to the *Legal RAG Bot*. Send any legal question and I will try to answer it.",
        parse_mode=ParseMode.MARKDOWN
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_question = update.message.text
    session_id = str(update.message.chat.id)  

    try:
        response = requests.post(
            API_URL,
            json={"query": user_question, "session_id": session_id},
            timeout=60
        )
        if response.status_code == 200:
            answer = response.json().get("answer", "No answer found.")
        else:
            answer = "Error: Unable to fetch answer from API."
    except Exception as e:
        answer = f"Error: {str(e)}"

    await update.message.reply_text(
        answer,
        parse_mode=ParseMode.MARKDOWN
    )

def build_app():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app
