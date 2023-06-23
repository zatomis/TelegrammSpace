import os
from urllib.parse import urlparse
import requests

def save_photo(url_image, name_image, path_image, url_param=""):
    os.makedirs(path_image,exist_ok = True)
    if url_param:
        response = requests.get(url_image, params={'api_key':url_param})
    else:
        response = requests.get(url_image)
    response.raise_for_status()
    with open(f"{path_image}{os.sep}{name_image}", 'wb') as file:
        file.write(response.content)
