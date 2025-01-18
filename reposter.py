import os
from io import BytesIO

import urllib.request
from time import sleep

import requests
from pyrogram.types import Message

import vk_parser
import pyrogram
import yt_dlp
import json
import re



with open('config.json') as config_file:
    config = json.load(config_file)

default_sleep_time = 5
error_sleep_time = 30
max_media_text_len = 1024
max_text_len = 4096
emoji = '🔥'

channel = '@' + config['CHANNEL_NAME']
vk_login = config['VK_LOGIN']
vk_password = config['VK_PASSWORD']

app_id = config['TELEGRAM_APP_API_ID']
app_hash = config['TELEGRAM_APP_API_HASH']
user_name = config['USER_NAME']

app = pyrogram.Client(user_name, app_id, app_hash)


def send_all_text(texts: list[str]) -> Message:
    mes = app.send_message(channel, texts[0], disable_web_page_preview=False)
    if len(texts) > 0:
        for txt in texts[1:]:
            mes = app.send_message(channel, txt, disable_web_page_preview=False,
                                   reply_to_message_id=mes.id)
    app.send_reaction(channel, mes.id, emoji)
    return mes


def main():
    app.start()

    data = vk_parser.get_last_post()
    while data is None:
        sleep(default_sleep_time)
        data = vk_parser.get_last_post()
    last_post = data

    while True:
        try:
            data = vk_parser.get_last_post()
            while data is None:
                sleep(default_sleep_time)
                data = vk_parser.get_last_post()

            if last_post is None or data.get('id') != last_post.get('id'):
                last_post = data
                media = []
                documents = []
                files = []
                is_other_media = False
                last_message = None

                text = re.sub('([#].+?)@nytrock', r'\1', data['text']).replace("#nytrock ", "")
                matches = re.findall(r"[[].+?[|].+?[]]", text)
                if matches:
                    for match in matches:
                        link_parts = match[1:-1].split('|')
                        link = f"<a href='https://vk.com/{link_parts[0]}'>{link_parts[1]}</a>"
                        text = text.replace(match, link)
                texts = [text]
                if len(text) > max_text_len:
                    texts = []
                    start = 0
                    end = max_text_len
                    for i in range(len(text) // max_text_len + 2):
                        if i != len(text) // max_text_len + 1:
                            end = text[:end].rfind(" ")
                        texts.append(text[start:min(end, len(text))])
                        start = end + 1
                        end += max_text_len

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
                            if len(text) < max_media_text_len:
                                last_message = app.send_animation(channel, attachment['doc']['url'], text)
                            else:
                                message = send_all_text(texts)
                                last_message = app.send_animation(channel, attachment['doc']['url'],
                                                                  reply_to_message_id=message.id)
                            is_other_media = True
                        else:
                            urllib.request.urlretrieve(attachment['doc']['url'], attachment['doc']['title'])
                            documents.append(pyrogram.types.InputMediaDocument(attachment['doc']['title']))
                            files.append(attachment['doc']['title'])

                    elif attachment['type'] == 'poll':
                        answers = list(map(lambda x: x['text'], attachment['poll']['answers']))
                        message = send_all_text(texts)
                        last_message = app.send_poll(channel, attachment['poll']['question'], answers,
                                                     reply_to_message_id=message.id)
                        is_other_media = True

                if is_other_media:
                    app.send_reaction(channel, last_message.id, emoji)
                    if documents:
                        app.send_media_group(channel, documents, reply_to_message_id=last_message.id)
                    continue

                print(1)
                if not media:
                    if documents:
                        documents[0].caption = text
                        app.send_media_group(channel, documents)
                    else:
                        send_all_text(texts)
                else:
                    print(2)
                    if len(text) < max_media_text_len:
                        print(3)
                        media[0].caption = text
                        last_message = app.send_media_group(channel, media)[0]
                        print(4)
                    else:
                        message = send_all_text(texts)
                        last_message = app.send_media_group(channel, media, reply_to_message_id=message.id)[0]
                    app.send_reaction(channel, last_message.id, emoji)

                    if documents:
                        app.send_media_group(channel, documents, reply_to_message_id=last_message.id)

                for file in files:
                    os.remove(file)
            sleep(default_sleep_time)
        except ConnectionResetError:
            sleep(error_sleep_time)


main()
