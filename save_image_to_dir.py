import os
from urllib.parse import urlparse
import requests

def image_save(url_image, name_image, path_image):
    os.makedirs(path_image,exist_ok = True)
    response = requests.get(url_image)
    response.raise_for_status()
    with open(f"{path_image}/{name_image}", 'wb') as file:
        file.write(response.content)
