import requests

import credentials

def get_token():

    client_id = credentials.client_id

    data = {
        "response_type": "token",
        "client_id": client_id
    }

    r = requests.get("https://oauth.yandex.com/authorize?", params= data)
    url = r.url

    print(url)