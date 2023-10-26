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
                            })

    return response.json()['response']['items'][0]


def get_all():
    response = requests.get("https://api.vk.com/method/wall.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'domain': domain,
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


def get_video(owner_id, video_id):
    response = requests.get("https://api.vk.com/method/video.get",
                            params={
                                'access_token': token,
                                'v': version,
                                'videos': f"{owner_id}_{video_id}"
                            })

    return response.json()['response']['items'][0]
