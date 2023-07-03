import requests
import os
import datetime
from urllib.parse import urlparse
import save_image_to_dir as save
import argparse


def get_extension(url):
    return os.path.splitext(urlparse(url).path)[1]


def day_time_now():
    dt = datetime.datetime.today()
    return f"{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}"


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count',  default='10', type=int, help='Кол-во фото для загрузки')
    return parser


def download_photos_of_launches(count):
    url = "https://api.spacexdata.com/v3/launches/"
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()
    for launch in launches[:count]:
        for index, space_url in enumerate(launch["links"]['flickr_images']):
            save.save_photo(space_url, f"img{index}{day_time_now()}.jpg", "LAUNCH")


if __name__ == '__main__':
    try:
        parser = create_parser()
        download_photos_of_launches(parser.parse_args().count)
    except requests.exceptions.HTTPError as error:
        print(f"Ошибка {error.response.text}")
