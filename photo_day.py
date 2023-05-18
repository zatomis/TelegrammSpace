import requests
import os
import json
from urllib.parse import urlparse
from dotenv import load_dotenv, find_dotenv
import save_image_to_dir as save

def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def photo_of_the_day(token, count):
    payload = {'count': f'{count}', 'api_key': f'{token}'}
    url = f"https://api.nasa.gov/planetary/apod"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for photo_number, photo_link in enumerate(response.json(), start=1):
        save.image_savedir(photo_link['url'], f"image_of_the_day{photo_number}.jpg", "IMAGE_DAY")

def photo_epic(token):
    payload = {'api_key': f'{token}'}
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    response = requests.get(url, params=payload)
    response.raise_for_status()
    for link_number, json_link in enumerate(response.json(), start=1):
        url = "https://api.nasa.gov/EPIC/archive/natural/" + str(json_link['date'].split(' ')[0]).replace("-", "/") + "/png/" + json_link['image'] + ".png?api_key=" + token
        save.image_savedir(url, f"Nasa{link_number}{get_extension(url)}", "IMAGE_EPIC")


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
            photo_of_the_day(token, 30)
            photo_epic(token)

        except requests.exceptions.HTTPError as error:
            print("Ошибка " + error.response.text)
