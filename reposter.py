from time import sleep

import requests

import vk_parser
import telebot
import json

with open('config.json') as file:
    config = json.load(file)

token = config['TELEGRAM_TOKEN']
channel = '@' + config['CHANNEL_NAME']
last_post = str()

bot = telebot.TeleBot(token)

while True:
    data = vk_parser.get_last_post()
    if data['text'] != last_post:
        text = data['text'].replace("@nytrock", "")

        for attachment in data['attachments']:
            if attachment['type'] == 'photo':
                image = requests.get(attachment['photo']['sizes'][-1]['url']).content
                bot.send_photo(channel, image, text)

        last_post = data['text']
    sleep(5)
