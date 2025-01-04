import requests
import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
import emoji
from googletrans import Translator

translator = Translator()

bot = telebot.TeleBot('7791090205:AAHEjfHReZ61oW-f_CYjJi9YLGmHJMIeU6M')

user_data = {}
history_data = {}


def choice_button():
    button_1 = KeyboardButton(text='Russian')
    button_2 = KeyboardButton(text='English')

    keyboard = ReplyKeyboardMarkup()
    keyboard.add(button_1, button_2)
    return keyboard


@bot.message_handler(commands=['start'])
def start(message):
    log_command(message, 'start')
    with open('gpt.png', 'rb') as photo:
        bot.send_photo(message.chat.id, photo=photo)
    bot.send_message(message.from_user.id,
                     'Please choose your native language.', reply_markup=choice_button())


@bot.message_handler(func=lambda message: message.text == "Russian")
def russian_answer(message):
    user_data[message.chat.id] = {"language": "Russian"}
    send_emoji = emoji.emojize(":grinning_face:")
    bot.send_message(message.from_user.id,
                     f"Привет! Я телеграмм бот, который может заменить тебе Chat GPT. Задавай мне любые вопросы.{send_emoji}",
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: message.text == "English")
def english_answer(message):
    user_data[message.chat.id] = {"language": "English"}
    send_emoji = emoji.emojize(":grinning_face:")
    bot.send_message(message.from_user.id,
                     f"Hello! I'am telegram bot, that can replace Chat GPT for you. Ask me any questions.{send_emoji}",
                     reply_markup=ReplyKeyboardRemove())


@bot.message_handler(func=lambda message: True)
def ask_question(message):
    if message.chat.id not in user_data:
        user_data[message.chat.id] = {"language": "English"}
    user_data[message.chat.id]['answer'] = message.text
    log_command(message, 'ask', {'question': message.text})
    send_answer(message.chat.id)


def send_answer(user_question):
    try:
        question = user_data[user_question]["answer"]
        response_data = get_response(question)
        if response_data and 'result' in response_data:
            content = response_data['result']
            if user_data[user_question]["language"] == "Russian":
                translated_content = translator.translate(content, src='en', dest='ru').text
                bot.send_message(user_question, f"Ответ: {translated_content}")
            else:
                bot.send_message(user_question, f"Answer: {content}")
        else:
            bot.send_message(user_question, "An error occurred while retrieving the response.")
    except Exception as e:
        bot.send_message(user_question, "An error occurred while processing your request. Please try again.")
        print("An error occurred:", str(e))


def get_response(question):
    try:
        url = "https://chatgpt-42.p.rapidapi.com/chatgpt"
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": question
                }
            ],
            "web_access": False
        }
        headers = {
            "x-rapidapi-key": "edac2fa23cmsh5279dfb3bc3a1c7p1034e1jsn9e9ee202dec5",
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("An error occurred while retrieving the response from API. Status code:", response.status_code)
            return None


    except Exception as e:
        print("An error occurred:", str(e))
        return None


@bot.message_handler(commands=['history'])
def history(message):
    chat_id = message.chat.id
    if chat_id in history_data and history_data[chat_id]:
        history_text = '\n'.join(
            [f"Command: {entry['command']}, Text: {entry['text']}" for entry in history_data[chat_id]])
        bot.send_message(chat_id, f'History of request: \n{history_text}')
    else:
        bot.send_message(chat_id, 'History of request is empty.')


def log_command(message, command, params=None):
    if params is None:
        params = {}
    chat_id = message.chat.id
    if chat_id not in history_data:
        history_data[chat_id] = []
    history_data[chat_id].append({'command': command, 'params': params, 'text': message.text})


bot.polling()
