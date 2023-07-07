import requests
import save_image_to_dir as save
import save_image_to_dir as get_data_time
import argparse


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--count',  default='10', type=int, help='Кол-во фото для загрузки')
    return parser


def download_photos_of_launches(count):
    url = "https://api.spacexdata.com/v3/launches/"
    response = requests.get(url)
    response.raise_for_status()
    launches = response.json()
    photo = []
    for launch in launches:
        for space_url in launch["links"]['flickr_images']:
            photo.append(space_url)
    for index, photo_url in enumerate(photo[:count]):
        save.save_photo(photo_url, f"img{index}{get_data_time.get_day_time_now()}.jpg", "LAUNCH")


if __name__ == '__main__':
    try:
        parser = create_parser()
        download_photos_of_launches(parser.parse_args().count)
    except requests.exceptions.HTTPError as error:
        print(f"Ошибка {error.response.text}")
