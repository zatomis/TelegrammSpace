import requests
import os
from urllib.parse import urlparse
from urllib.error import URLError
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save
import argparse
import datetime


def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def day_time_now():
    dt = datetime.datetime.today()
    return f"{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}"


def get_photo_today(token, count_photo):
    payload = {'count': count_photo, 'api_key': token}
    url = f"https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for photo_number, photo_link in enumerate(response.json(), start=1):
        try:
            save.save_photo(photo_link['url'], f"img_of_the_day{photo_number}{day_time_now()}.jpg", "IMAGE_DAY")
        except URLError as error:
            print(f"{error}\nНе верный адрес для загрузки фото {photo_link['url']}")


def create_parser():
    parser_arg = argparse.ArgumentParser()
    parser_arg.add_argument('-c', '--count',  default='30', type=int, help='Кол-во фото для загрузки')
    return parser


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("NASA_SPACE_KEY", "ERROR")
    parser = create_parser()
    count = parser.parse_args().count
    if token == "ERROR":
        print("Не указан токен https://api.nasa.gov/#apod")
    else:
        try:
            get_photo_today(token, count)
        except requests.exceptions.HTTPError as error:
            print(f"Ошибка {error.response.text}")
