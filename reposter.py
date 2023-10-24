from time import sleep

import vk_parser
import telebot

token = ""
login = "@nytrock"
last_post = str()

while True:
    data = vk_parser.get_last_post()
    if data['text'] != last_post:
        print("NEW")
        last_post = data['text']
    sleep(5)
