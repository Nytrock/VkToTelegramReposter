import os
from time import sleep

import requests

import vk_parser
import telebot
import yt_dlp
import json
import glob

with open('config.json') as file:
    config = json.load(file)

token = config['TELEGRAM_TOKEN']
channel = '@' + config['CHANNEL_NAME']
vk_login = config["VK_LOGIN"]
vk_password = config["VK_PASSWORD"]
last_post = str()

bot = telebot.TeleBot(token)

while True:
    data = vk_parser.get_by_id(13)
    if data['text'] != last_post:
        text = data['text'].replace("@nytrock", "")

        for attachment in data['attachments']:
            if attachment['type'] == 'photo':
                sizes = {}
                for size in attachment['photo']['sizes']:
                    sizes[size['type']] = size['url']

                url = str()
                if 'w' in sizes.keys():
                    url = sizes['w']
                elif 'z' in sizes.keys():
                    url = sizes['z']
                elif 'y' in sizes.keys():
                    url = sizes['y']
                elif 'x' in sizes.keys():
                    url = sizes['x']
                elif 'm' in sizes.keys():
                    url = sizes['m']

                image = requests.get(url).content
                bot.send_photo(channel, image, text)
            elif attachment['type'] == 'video':
                ydl_opts = {"username": vk_login, "password": vk_password}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://vk.com/"
                                  f"video{attachment['video']['owner_id']}_{attachment['video']['id']}"])
                file_name = glob.glob('*.mp4')[0]
                with open(file_name, 'rb') as video:
                    message = bot.send_message(channel, text)
                    bot.send_video(channel, video, reply_to_message_id=message.message_id)
                os.remove(file_name)
            elif attachment['type'] == 'doc':
                if attachment['doc']['ext'] == 'gif':
                    bot.send_animation(channel, attachment['doc']['url'], caption=text)

        last_post = data['text']
    sleep(5)
