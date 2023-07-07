import requests
import os
from urllib.error import URLError
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save
import save_image_to_dir as get_data_time
import argparse


def get_photo_today(token, photo_count):
    payload = {'count': photo_count, 'api_key': token}
    url = f"https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for photo_number, photo_link in enumerate(response.json(), start=1):
        try:
            save.save_photo(photo_link['url'], f"img_of_the_day{photo_number}{get_data_time.get_day_time_now()}.jpg",
                            "IMAGE_DAY")
        except URLError as error:
            print(f"{error}\nНе верный адрес для загрузки фото {photo_link['url']}")


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count',  default='30', type=int, help='Кол-во фото для загрузки')
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
