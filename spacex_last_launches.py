import requests
import os
import json
from urllib.parse import urlparse
import save_image_to_dir as save

def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    response.raise_for_status()
    try:
        for total_links in range(1,len(response.json())):
            response = requests.get(f"{url}{str(total_links)}")
            response.raise_for_status()
            links = response.json()["links"]['flickr_images']
            for link_number, link in enumerate(links, start=1):
                save.image_save(link, f"image{total_links}{link_number}.jpg", "LAUNCH")

    except requests.exceptions.HTTPError as error:
        print("Ошибка " + error.response.text)

if __name__ == '__main__':
    try:
        fetch_spacex_last_launch("https://api.spacexdata.com/v3/launches/")
    except requests.exceptions.HTTPError as error:
        print("Ошибка " + error.response.text)
