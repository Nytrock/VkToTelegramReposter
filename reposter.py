import os
from io import BytesIO
from time import sleep

import urllib.request
import requests

import vk_parser
import pyrogram
import yt_dlp
import json
import re


def send_all_text():
    mes = app.send_message(channel, texts[0], disable_web_page_preview=False)
    if len(texts) > 0:
        for txt in texts[1:]:
            mes = app.send_message(channel, txt, disable_web_page_preview=False,
                                   reply_to_message_id=mes.id)
    return mes


with open('config.json') as file:
    config = json.load(file)

default_sleep_time = 5
error_sleep_time = 30

channel = '@' + config['CHANNEL_NAME']
vk_login = config["VK_LOGIN"]
vk_password = config["VK_PASSWORD"]

app_id = config['TELEGRAM_APP_API_ID']
app_hash = config['TELEGRAM_APP_API_HASH']
user_name = config['USER_NAME']

app = pyrogram.Client(user_name, app_id, app_hash)
app.start()
data = vk_parser.get_last_post()
while data is None:
    sleep(default_sleep_time)
    data = vk_parser.get_last_post()

last_post = data['text']

while True:
    try:
        data = vk_parser.get_last_post()
        while data is None:
            sleep(default_sleep_time)
            data = vk_parser.get_last_post()

        if data['text'] != last_post:
            last_post = data['text']
            media = []
            documents = []
            files = []
            isOtherMedia = False
            last_message = None

            text = re.sub('([#].+?)@nytrock', r'\1', data['text']).replace("#nytrock ", "")
            matches = re.findall(r"[[].+?[|].+?[]]", text)
            if matches:
                for match in matches:
                    link_parts = match[1:-1].split('|')
                    link = f"<a href='https://vk.com/{link_parts[0]}'>{link_parts[1]}</a>"
                    text = text.replace(match, link)
            texts = [text]
            if len(text) > 4096:
                texts = []
                start = 0
                end = 4096
                for i in range(len(text) // 4096 + 2):
                    if i != len(text) // 4096 + 1:
                        end = text[:end].rfind(" ")
                    texts.append(text[start:min(end, len(text))])
                    start = end + 1
                    end += 4096

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
                    media.append(pyrogram.types.InputMediaPhoto(BytesIO(image)))
                elif attachment['type'] == 'video':
                    link = f"https://vk.com/video{attachment['video']['owner_id']}_{attachment['video']['id']}"
                    file_name = link.split("/")[-1] + ".mp4"
                    ydl_opts = {"username": vk_login, "password": vk_password, "outtmpl": file_name}

                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([link])

                    media.append(pyrogram.types.InputMediaVideo(file_name))
                    files.append(file_name)
                elif attachment['type'] == 'doc':
                    if attachment['doc']['ext'] == 'gif':
                        if len(text) < 1024:
                            app.send_animation(channel, attachment['doc']['url'], text)
                        else:
                            message = send_all_text()
                            last_message = app.send_animation(channel, attachment['doc']['url'],
                                                              reply_to_message_id=message.id)
                        isOtherMedia = True
                    else:
                        urllib.request.urlretrieve(attachment['doc']['url'], attachment['doc']['title'])
                        documents.append(pyrogram.types.InputMediaDocument(attachment['doc']['title']))
                        files.append(attachment['doc']['title'])

                elif attachment['type'] == 'poll':
                    answers = list(map(lambda x: x['text'], attachment['poll']['answers']))
                    message = send_all_text()
                    last_message = app.send_poll(channel, attachment['poll']['question'], answers,
                                                 reply_to_message_id=message.id)
                    isOtherMedia = True

            if isOtherMedia:
                if documents:
                    app.send_media_group(channel, documents, reply_to_message_id=last_message.id)
                continue

            if not media:
                if documents:
                    documents[0].caption = text
                    app.send_media_group(channel, documents)
                else:
                    app.send_message(channel, text)
            else:
                if len(text) < 1024:
                    media[0].caption = text
                    last_message = app.send_media_group(channel, media)[0]
                else:
                    message = send_all_text()
                    last_message = app.send_media_group(channel, media, reply_to_message_id=message.id)[0]

                if documents:
                    app.send_media_group(channel, documents, reply_to_message_id=last_message.id)

            for file in files:
                os.remove(file)

        sleep(default_sleep_time)
    except ConnectionResetError:
        sleep(error_sleep_time)
