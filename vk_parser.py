import requests

token = ""
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

    return response.json()['response']['items'][0]['text']
