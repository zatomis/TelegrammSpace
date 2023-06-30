import requests
import os
from urllib.parse import urlparse
import save_image_to_dir as save

def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def download_photos_of_launches():
    url = "https://api.spacexdata.com/v3/launches/"
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()
    for launch in launches:
        for index, space_url in enumerate(launch["links"]['flickr_images']):
            save.save_photo(space_url, f"image{index}.jpg", "LAUNCH")


if __name__ == '__main__':
    try:
        download_photos_of_launches()
    except requests.exceptions.HTTPError as error:
        print(f"Ошибка {error.response.text}")
