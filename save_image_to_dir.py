import os
import requests


def save_photo(url_image, name_image, path_image, params=None):
    os.makedirs(path_image, exist_ok=True)
    response = requests.get(url_image, params)
    response.raise_for_status()
    with open(f"{path_image}{os.sep}{name_image}", 'wb') as file:
        file.write(response.content)
