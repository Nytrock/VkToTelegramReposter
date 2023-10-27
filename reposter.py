import os
from time import sleep

import requests

import vk_parser
import pyrogram
import yt_dlp
import json
import glob

with open('config.json') as file:
    config = json.load(file)

channel = '@' + config['CHANNEL_NAME']
vk_login = config["VK_LOGIN"]
vk_password = config["VK_PASSWORD"]
last_post = str()

app_id = config['TELEGRAM_APP_API_ID']
app_hash = config['TELEGRAM_APP_API_HASH']
user_name = config['USER_NAME']

app = pyrogram.Client(user_name, app_id, app_hash)
app.start()

while True:
    data = vk_parser.get_by_id(7)
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
                app.send_photo(channel, url, text)
            elif attachment['type'] == 'video':
                ydl_opts = {"username": vk_login, "password": vk_password}
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([f"https://vk.com/"
                                  f"video{attachment['video']['owner_id']}_{attachment['video']['id']}"])
                file_name = glob.glob('*.mp4')[0]
                with open(file_name, 'rb') as video:
                    message = app.send_message(channel, text)
                    app.send_video(channel, video, reply_to_message_id=message.id)
                os.remove(file_name)
            elif attachment['type'] == 'doc':
                if attachment['doc']['ext'] == 'gif':
                    app.send_animation(channel, attachment['doc']['url'], caption=text)

        last_post = data['text']
    sleep(5)
