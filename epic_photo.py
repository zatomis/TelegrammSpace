import requests
import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save


def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def photo_epic(token):
    payload = {'api_key': f'{token}'}
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for link_number, json_link in enumerate(response.json(), start=1):
        url = f"https://api.nasa.gov/EPIC/archive/natural/{str(json_link['date'].split(' ')[0]).replace('-','/')}/png/{json_link['image']}.png?api_key={token}"
        save.image_save(url, f"Nasa{link_number}{get_extension(url)}", "IMAGE_EPIC")


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("NASA_SPACE_KEY", "ERROR")

    if token == "ERROR":
        print("Не указан токен https://api.nasa.gov/#apod")
    else:
        try:
            photo_epic(token)
        except requests.exceptions.HTTPError as error:
            print("Ошибка " + error.response.text)
