import requests
import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save
from datetime import datetime


def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def get_epic_photo(token):
    payload = {'api_key': token}
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for link_number, json_link in enumerate(response.json(), start=1):
        date_iso = datetime.fromisoformat(json_link['date']).strftime('%Y/%m/%d')
        # url = f"https://api.nasa.gov/EPIC/archive/natural/{date_iso}/png/{json_link['image']}.png?api_key={token}"
        url = f"https://api.nasa.gov/EPIC/archive/natural/{date_iso}/png/{json_link['image']}.png"
        save.image_save(url, f"Nasa{link_number}{get_extension(url)}", "IMAGE_EPIC", token)


if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("NASA_SPACE_KEY", "ERROR")

    if token == "ERROR":
        print("Не указан токен https://api.nasa.gov/#apod")
    else:
        try:
            get_epic_photo(token)
        except requests.exceptions.HTTPError as error:
            print("Ошибка " + error.response.text)
