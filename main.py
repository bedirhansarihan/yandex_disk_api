import logging




from YandexClient import YandexClient
from get_access_token import get_token
from credentials import client_id, client_secret, token


logger = logging.getLogger()

logger.setLevel(logging.INFO)

stream_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s %(levelname)s :: %(message)s')
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

file_handler = logging.FileHandler('info.log')
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

logger.addHandler(stream_handler)
logger.addHandler(file_handler)

## TEST
if __name__ == '__main__':

    # add your token into "credential.py"

    if token == "":

        # if you don't have a token, get it from the link and add it into "credential.py"
        get_token()

        yandex = YandexClient(client_id, client_secret, token)