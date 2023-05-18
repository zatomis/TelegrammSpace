import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import telegram


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("TELEGRAMBOT_KEY", "ERROR")

    if token == "ERROR":
        print("Не указан бот токен см. https://t.me/botfather")
    else:
        bot = telegram.Bot(token=token)
        bot.send_message(chat_id="@publics900", text="I'm sorry Dave I'm afraid I can't do that.")
        bot.send_document(chat_id="@publics900", document=open('LAUNCH/image132.jpg', 'rb'))
