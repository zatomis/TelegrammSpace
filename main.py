import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import telegram
import random
import time
import argparse

TIME_DELAY = 4*60*60

def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--freq')
    return parser

def check_photo_file(path):
    photo_ext = ['jpg', 'png', 'bmp', 'gif']
    if (str(os.path.splitext(urlparse(path).path)[1]).replace(".","") in photo_ext) and (os.stat(path).st_size<20000000):
        return True
    else:
        return False

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("TELEGRAMBOT_KEY", "ERROR")
    telegram_chanel = os.environ.get("TELEGRAMBOTGROUP", "ERROR")
    parser = create_parser()
    if(parser.parse_args().freq):
        frequency = parser.parse_args().freq
        if token == "ERROR":
            print("Не указан бот токен см. https://t.me/botfather")
        else:
            image_list = []
            for address, dirs, files in os.walk(os.path.abspath(os.curdir)):
                for name in files:
                    photo_file = os.path.join(address, name)
                    if check_photo_file(photo_file):
                        image_list.append(photo_file)
            bot = telegram.Bot(token=token)
            while True:
                bot.send_document(chat_id=telegram_chanel, document=open(random.choice(image_list), 'rb'))
                time.sleep(int(int(TIME_DELAY)/int(frequency)))
    else:
        print("Не указан параметр частоты запуска скрипта -f")

