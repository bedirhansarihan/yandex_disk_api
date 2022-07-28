import logging
from YandexClient import YandexClient
logger = logging.getLogger()

logger.setLevel(logging.INFO)
#import pandas as pd

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)


if __name__ == '__main__':

    yandex = YandexClient("public_key", "secret_key")


    yandex.download_file_from_yandex(path="disk:/test.jpg")
