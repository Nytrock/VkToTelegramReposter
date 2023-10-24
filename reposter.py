
from time import sleep

import vk_parser
import telebot
import json

with open("config.json") as file:
    config = json.load(file)

token = config["TELEGRAM_TOKEN"]
login = "@" + config["CHANNEL_NAME"]
last_post = str()

while True:
    data = vk_parser.get_last_post()
    if data['text'] != last_post:
        print("NEW")
        last_post = data['text']
    sleep(5)
