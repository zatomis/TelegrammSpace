import requests
import os
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save

def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def get_photo_today(token, count):
    payload = {'count': count, 'api_key': token}
    url = f"https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for photo_number, photo_link in enumerate(response.json(), start=1):
        try:
            save.save_photo(photo_link['url'], f"image_of_the_day{photo_number}.jpg", "IMAGE_DAY")
        except:
            print(f"Не верный адрес для загрузки фото {photo_link['url']}")


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("NASA_SPACE_KEY", "ERROR")

    if token == "ERROR":
        print("Не указан токен https://api.nasa.gov/#apod")
    else:
        try:
            get_photo_today(token, 30)
        except requests.exceptions.HTTPError as error:
            print(f"Ошибка {error.response.text}")
