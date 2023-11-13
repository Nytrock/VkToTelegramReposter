# VK to Telegram reposter
This bot allows you to automatically forward posts from a selected VKontakte group to a selected Telegram channel. Main advantages of the application:
- Flexible setup
- Support for pictures, videos, files, gifs attached to posts
- Automatic division of text into blocks when the character limit in a message is exceeded
- Support for links in words of text and polls
- When the connection to the Internet is interrupted, the program automatically turns off and turns on when the network appears

# Instructions for use
- Clone the repository

```shell
git clone https://github.com/Nytrock/VkToTelegramReposter.git
```

- Install dependencies with requirements.txt
```shell
pip install -r requirements.txt
```

- Create `config.json` file in the folder and fill it like this:
```shell
{
   "VK_TOKEN": "Access key to VKontakte API",
   "TELEGRAM_APP_API_ID": "Telegram application ID",
   "TELEGRAM_APP_API_HASH": "Telegram application hash",
   "CHANNEL_NAME": "Name of the channel in Telegram",
   "USER_NAME": "Telegram username",
   "VK_LOGIN": "User login on VKontakte",
   "VK_PASSWORD": "User password on VKontakte"
}
```
You need to create a Telegram application through [this site](https://my.telegram.org) and get a VK access token (instruction [here](https://dev.vk.com/ru/api/access-token/getting-started)). 
How to fill in the remaining fields is intuitive.

- Run script `reposter.py`

- While the script is running, the program will run continuously
