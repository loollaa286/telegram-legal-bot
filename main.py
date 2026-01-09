from app.bot import build_app

if __name__ == "__main__":
    bot_app = build_app()
    bot_app.run_polling()
