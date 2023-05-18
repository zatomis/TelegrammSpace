import os
from urllib.parse import urlparse
import requests

def image_savedir(url_image, name_image, path_image):
    if not os.path.exists(path_image):
        os.makedirs(path_image)
    print("url_image " + url_image + "\nurl_ext " + os.path.splitext(urlparse(url_image).path)[1] + "\nname_image " + name_image + "\npath_image " + path_image + "\n=====================")
    response = requests.get(url_image)
    response.raise_for_status()
    try:
        with open(path_image + "/" + name_image, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.HTTPError as error:
        print("Ошибка " + error.response.text)
