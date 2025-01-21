# Telegram Bot: ChatGPT Assistant
This repository contains a Python script for a Telegram bot that acts as an assistant, allowing users to interact with a GPT-like API for answers to their queries. The bot supports English, Russian and Polish languages, logs user interactions, and provides a history of commands.


## Features

**1. Language Selection:**

- Users can select their preferred language: Russian, English or Polish.
- The bot translates answers into the selected language.

**2. Question Handling:**

- Users can ask any question, and the bot fetches responses from the ChatGPT API.
- Responses are adapted to the user's chosen language.

**3.Command History:**

- The bot logs all user interactions.
- Users can retrieve their command history using the /history command.

**4. Error Handling:**

- Handles API errors gracefully, providing users with helpful error messages.

**5. Emoji Integration:**

- Adds a friendly touch to bot messages using emojis.

**6. MySQL Database Integration:**

- The bot uses a MySQL database to store user language preferences and track their usage.
- Language usage statistics are analyzed to determine which languages are most frequently selected.
- This analysis can guide future improvements to the bot's functionality, such as adding support for additional languages or optimizing translation performance.


## How to Set Up
#### Prerequisites
- Python 3.8 or higher.
- Telegram bot token from BotFather.
- RapidAPI key for accessing the GPT API.
- MySQL database setup.


#### Installation

**1. Clone the repository:**
```sh
bash
git clone https://github.com/diankaaaa21/Telegram_Bot_Assistant.git
cd Telegram Bot Assistant
```

**2. Install required libraries:**

The bot requires several Python libraries. You can install them using pip:
```sh
bash
pip install requests pytelegrambotapi googletrans emoji pyTelegramBotAPI python-dotenv 
```

**3. Set up MySQL database:**

Create a database and table for storing language preferences:

```sh
CREATE DATABASE telegram_bot;
USE telegram_bot;

CREATE TABLE telegram_users (
    user_id BIGINT PRIMARY KEY,
    language VARCHAR(50)
);
```

**4. Create a .env file:**

In the root directory, add the following:

```sh
TELEGRAM_BOT_TOKEN=your_telegram_bot_token
API_KEY=your_rapidapi_key
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_NAME=telegram_bot
```

**5. Set up the environment:**

- Replace the bot token in the script:
```sh
python
bot = telebot.TeleBot('YOUR_TELEGRAM_BOT_TOKEN')
```
- Replace the RapidAPI key:
```sh
python
headers = {
    "x-rapidapi-key": "YOUR_RAPIDAPI_KEY",
    "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
    "Content-Type": "application/json"
}
```

**6. Add the required image (gpt.png) for the /start command in the same directory.**

## Running the Bot
Run the script using Python:
```sh
bash
python bot.py
```


## Commands
- /start:
Initiates interaction with the bot and prompts the user to choose their preferred language.
- /history: 
Displays the user's command history, including the commands and associated texts.
- statistics:
(Optional) Displays language usage statistics stored in the MySQL database.


## MySQL Database Usage
The bot uses a MySQL database for two main purposes:

**1. Storing User Language Preferences:**
- When a user selects a language, it is stored in the telegram_users table.
- If the user changes their language, the record is updated using ON DUPLICATE KEY.

**2. Language Usage Analysis:**
- The database aggregates statistics on the frequency of language selection.
- The /statistics command retrieves this data, helping to identify which languages are most popular.
- This information can guide future improvements to the bot, such as adding new language support or enhancing translation quality.
Example SQL query for statistics:
```sh
SELECT language, COUNT(*) AS count
FROM telegram_users
GROUP BY language
ORDER BY count DESC;
```


## Logging

The bot logs all key events in the stderr.txt file. If there are any errors or problems with the API, you will find detailed information in this file.
#### Possible Errors
- API Error: If the API is unresponsive or there is a network issue, the bot will display an error message.
- Missing Tokens: If the .env file does not contain values for TELEGRAM_BOT_TOKEN or API_KEY, the bot will terminate with an error.


## Code Overview

#### Main Components

**1. Language Selection:**

- The bot provides buttons for Russian, English and Polish using a custom keyboard.
- User language preference is saved in a dictionary (user_data).

**2. Question Handling:**

- The bot accepts free-text questions and forwards them to the ChatGPT API.
- Responses are translated into Russian if required.

**3. History Logging:**

- Each interaction is logged in a history_data dictionary.
- The /history command retrieves and displays this information.

**4. API Integration:**

- Utilizes the RapidAPI endpoint for querying GPT responses.

#### Error Handling
- Logs API and bot errors to the console.
- Notifies users if something goes wrong.


## Example Interaction

1. User sends /start:
```sh
css
Please choose your native language.
[ Russian ] [ English ] [ Polish ]
```
2. User selects Russian:
```sh
Привет! Я телеграмм бот, который может заменить тебе Chat GPT. Задавай мне любые вопросы. 😊
```
3. User selects English:
```sh
Hello! I'am telegram bot, that can replace Chat GPT for you. Ask me any questions. 😊
```
4. User selects Polish:
```sh
Hello! I'am telegram bot, that can replace Chat GPT for you. Ask me any questions. 😊
```
5. User asks a question:
```sh
makefile
What is the sense of life?
Answer: The sense of life depends on your goals and values.
```
6. User retrieves history:
```sh
yaml
/history
History of request: 
Command: start, Text: /start
Command: ask, Text: What is the sense of life?
```

## Dependencies
- **requests**: For making API requests.
- **pyTelegramBotAPI**: For Telegram bot functionality.
- **googletrans**: For translating responses.
- **emoji**: For adding emojis to messages.
- **mysql-connector-python:** For MySQL database integration.
- **python-dotenv:** For managing environment variables.


## Notes
1. Ensure the gpt.png file exists in the working directory for the /start command.
2. Avoid sharing your bot token and API key publicly.
3. The bot currently supports a limited set of languages for translation.
4. Regulary back up your database to prevent data loss.


## Contributing
Contributions are welcome! Feel free to open issues or submit pull requests to improve functionality or fix bugs.

## License
This project is licensed under the MIT License.
