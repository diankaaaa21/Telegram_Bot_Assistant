import os

import requests
import telebot
from dotenv import load_dotenv
from googletrans import Translator
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from database import logger, save_language
from file_log import configurate_logger

logger = configurate_logger()
load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
KEY = os.getenv("API_KEY")
translator = Translator()

if not TOKEN or not KEY:
    logger.critical(
        "TELEGRAM_BOT_TOKEN or API_KEY is missing in environment variables."
    )
    raise ValueError("TELEGRAM_BOT_TOKEN or API_KEY is missing")

bot = telebot.TeleBot(TOKEN)

user_data = {}
history_data = {}


def choice_button():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(
        KeyboardButton("Russian"), KeyboardButton("English"), KeyboardButton("Polish")
    )
    return keyboard


@bot.message_handler(commands=["start"])
def start(message):
    log_command(message, "start")

    if os.path.exists("gpt.png"):
        with open("gpt.png", "rb") as photo:
            bot.send_photo(message.chat.id, photo=photo)
    else:
        logger.warning('Image "gpt.png" not found. Skipping photo.')

    bot.send_message(
        message.chat.id,
        "Please choose your native language.",
        reply_markup=choice_button(),
    )


def set_language(message, language, greeting):
    user_data[message.chat.id] = {"language": language}
    save_language(message.chat.id, language)
    bot.send_message(message.chat.id, greeting, reply_markup=ReplyKeyboardRemove())


@bot.message_handler(
    func=lambda message: message.text in ["Russian", "English", "Polish"]
)
def language_selection(message):
    greetings = {
        "Russian": "Привет! Я телеграмм бот, который может заменить тебе Chat GPT. Задавай мне любые вопросы. 😊",
        "English": "Hello! I'm a Telegram bot that can replace ChatGPT for you. Ask me any questions. 😊",
        "Polish": "Cześć! Jestem botem Telegram, który może zastąpić Ci ChatGPT. Zadaj mi pytania. 😊",
    }
    set_language(message, message.text, greetings[message.text])


@bot.message_handler(func=lambda message: True)
def ask_question(message):
    """Обрабатывает вопросы пользователя и отправляет их на API."""
    chat_id = message.chat.id
    if chat_id not in user_data:
        user_data[chat_id] = {"language": "English"}

    user_data[chat_id]["answer"] = message.text
    log_command(message, "ask", {"question": message.text})
    send_answer(chat_id)


def send_answer(chat_id):
    try:
        question = user_data[chat_id]["answer"]
        response_data = get_response(question)

        if response_data and "result" in response_data:
            content = response_data["result"]
            user_lang = user_data[chat_id]["language"]

            if user_lang in ["Russian", "Polish"]:
                try:
                    lang_code = "ru" if user_lang == "Russian" else "pl"
                    translated_content = translator.translate(
                        content, src="en", dest=lang_code
                    ).text
                except Exception as e:
                    logger.warning(f"Translation failed: {e}")
                    bot.send_message(
                        chat_id, "Translation error. Sending the response in English."
                    )
                    translated_content = content
                bot.send_message(
                    chat_id,
                    (
                        f"Ответ: {translated_content}"
                        if user_lang == "Russian"
                        else f"Odpowiedź: {translated_content}"
                    ),
                )
            else:
                bot.send_message(chat_id, f"Answer: {content}")

        else:
            logger.error("Empty or invalid response from API")
            bot.send_message(
                chat_id, "An error occurred while retrieving the response."
            )

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        bot.send_message(
            chat_id,
            "An error occurred while processing your request. Please try again.",
        )


def get_response(question):
    try:
        url = "https://chatgpt-42.p.rapidapi.com/chatgpt"
        payload = {
            "messages": [{"role": "user", "content": question}],
            "web_access": False,
        }
        headers = {
            "x-rapidapi-key": KEY,
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json",
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API error. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        logger.error(f"API request error: {e}")
        return None


@bot.message_handler(commands=["history"])
def history(message):
    chat_id = message.chat.id
    if chat_id in history_data and history_data[chat_id]:
        history_text = "\n".join(
            [
                f"Command: {entry['command']}, Text: {entry['text']}"
                for entry in history_data[chat_id]
            ]
        )
        bot.send_message(chat_id, f"History of requests:\n{history_text}")
    else:
        bot.send_message(chat_id, "History of requests is empty.")


def log_command(message, command, params=None):
    if params is None:
        params = {}

    chat_id = message.chat.id
    if chat_id not in history_data:
        history_data[chat_id] = []

    history_data[chat_id].append(
        {"command": command, "params": params, "text": message.text}
    )


@bot.message_handler(commands=["statistics"])
def statistics(message):
    stats = get_statistics()
    if stats:
        stats_message = "\n".join([f"{row[0]}: {row[1]}" for row in stats])
        bot.send_message(
            message.chat.id, f"Language selection statistics:\n{stats_message}"
        )
    else:
        bot.send_message(message.chat.id, "No statistics available.")


def get_statistics():
    return [("Russian", 5), ("English", 10), ("Polish", 3)]


if __name__ == "__main__":
    logger.info("Bot is running.")
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logger.critical(f"Critical error in polling: {e}")
