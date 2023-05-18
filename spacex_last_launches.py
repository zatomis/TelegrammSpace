import requests
import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save

def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    response.raise_for_status()
    try:
        total_links = 1
        while total_links <= len(response.json()):
            response = requests.get(url+str(total_links))
            response.raise_for_status()
            links = response.json()["links"]['flickr_images']
            for link_number, link in enumerate(links, start=1):
                save.image_savedir(link, f"image{total_links}{link_number}.jpg", "LAUNCH")
            total_links = total_links + 1
    except requests.exceptions.HTTPError as error:
        print("Ошибка " + error.response.text)

if __name__ == '__main__':
    load_dotenv(find_dotenv())
    token = os.environ.get("NASA_SPACE_KEY", "ERROR")

    if token == "ERROR":
        print("Не указан токен https://api.nasa.gov/#apod")
    else:
        try:
            fetch_spacex_last_launch("https://api.spacexdata.com/v3/launches/")

        except requests.exceptions.HTTPError as error:
            print("Ошибка " + error.response.text)
