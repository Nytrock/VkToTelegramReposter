import requests
import json

with open("config.json") as file:
    config = json.load(file)

token = config["VK_TOKEN"]
version = 5.154
domain = "nytrock"


def get_last_post():
    response = requests.get("https://api.vk.com/method/wall.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': 1
                            }).json()['response']['items'][0]

    if 'is_pinned' in response:
        response = get_by_id(2)

    return response


def get_all(offset=0):
    response = requests.get("https://api.vk.com/method/wall.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'offset': offset
                            })

    return response.json()['response']['items']


def get_by_id(num):
    response = requests.get("https://api.vk.com/method/wall.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': 1,
                                'offset': num - 1
                            })

    return response.json()['response']['items'][0]
