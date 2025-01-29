import os

from flask import Flask, request
from telegram import Update

from telegram_bot import TOKEN, bot

app = Flask(__name__)


@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(), bot)
    bot.process_new_updates([update])
    return "OK", 200


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"http://<question>.ngrok.io/{TOKEN}")
    app.run(host="0.0.0.0", port=5000)
