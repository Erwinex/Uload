# Uload

Uload is a cool Telegram bot based on [Pyrogram](https://github.com/pyrogram/pyrogram) that can upload your file in that and it will give you a link to you to accesse the file via the bot.

## Some features

- Via Uload you can look channel(channels) and it force the user to join to the channel to get the file
- You can send a message to all bot users
- and so on ...

## Preparation

All you need is just installing [Pyrogram](https://github.com/pyrogram/pyrogram) package and Tgcrypto for better performance(optional) via pip here is what you should do :

`pip3 install -U pyrogram tgcrypto`

## Bot configuration

All you need is to edit main.py and plugins/menu_handler.py files and here is how

### main.py:

line 10 to 15

```
app = Client(name="Uload", # You can change it if you'd like to
             api_id= int(), # Replace it with your own one
             api_hash="", # Replace it with your own one
             plugins=plugins_dir,
             bot_token="" # Replace it with your own one
             )
```

You just need to edit this part in this file

### plugins/menu_handler.py:

line 12

```
storage_chat_id = int("-1002222222222") # Fill it with the chat id that you want the bot to save the files in it group, channel or ... channel is perferd.
```

you just need to edit this part

## How to run the bot

You can run the bot with the command
`python3 main.py`

## Also read this

I know it can be way more better than it is so if did any change thing and made it better you can always share it whit others 🙂
