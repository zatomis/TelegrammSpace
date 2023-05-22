import requests
import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save

def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def photo_today(token, count):
    payload = {'count': f'{count}', 'api_key': f'{token}'}
    url = f"https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for photo_number, photo_link in enumerate(response.json(), start=1):
        save.image_save(photo_link['url'], f"image_of_the_day{photo_number}.jpg", "IMAGE_DAY")


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("NASA_SPACE_KEY", "ERROR")

    if token == "ERROR":
        print("Не указан токен https://api.nasa.gov/#apod")
    else:
        try:
            photo_today(token, 30)
        except requests.exceptions.HTTPError as error:
            print("Ошибка " + error.response.text)
