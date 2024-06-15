from time import sleep

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
                            }).json()
    if 'response' not in response.keys():
        return None
    response = response['response']['items'][0]

    if 'is_pinned' in response:
        next_response = get_by_id(2)
        while next_response is None:
            sleep(5)
            next_response = get_by_id(2)

        if next_response['date'] > response['date']:
            response = next_response

    return response


def get_all(offset=0):
    response = requests.get("https://api.vk.com/method/wall.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'offset': offset
                            }).json()

    if 'response' not in response.keys():
        return None

    return response['response']['items']


def get_by_id(num):
    response = requests.get("https://api.vk.com/method/wall.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
                                'count': 1,
                                'offset': num - 1
                            }).json()

    if 'response' not in response.keys():
        return None

    return response['response']['items'][0]
