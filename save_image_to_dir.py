import os
import requests
import datetime


def get_day_time_now():
    dt = datetime.datetime.today()
    return f"{dt.year}{dt.month}{dt.day}{dt.hour}{dt.minute}"


def save_photo(url_image, name_image, path_image, params=None):
    os.makedirs(path_image, exist_ok=True)
    response = requests.get(url_image, params)
    response.raise_for_status()
    with open(f"{path_image}{os.sep}{name_image}", 'wb') as file:
        file.write(response.content)
