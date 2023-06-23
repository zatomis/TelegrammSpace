import requests
import os
import json
from urllib.parse import urlparse
import save_image_to_dir as save

def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def download_photos_of_launches(url):
    response = requests.get(url)
    response.raise_for_status()
    for flight_number in range(1,len(response.json())):
        response = requests.get(url+str(flight_number))
        response.raise_for_status()
        links = response.json()["links"]['flickr_images']
        for link_number, link in enumerate(links, start=1):
            save.save_photo(link, f"image{flight_number}{link_number}.jpg", "LAUNCH")


if __name__ == '__main__':
    try:
        download_photos_of_launches("https://api.spacexdata.com/v3/launches/")
    except requests.exceptions.HTTPError as error:
        print(f"Ошибка {error.response.text}")
