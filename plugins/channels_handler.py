from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3
import Forward_noquote_messages
from Database_code import db
import Custom_filters
import asyncio
from User_step import user_step


async def countdown(seconds):
    for i in range(seconds, 0, -1):
        await asyncio.sleep(1)
    return True


@Client.on_message(filters.regex("Chats list 📢") & filters.private & Custom_filters.admin)
async def get_chats_list(client: Client, message: Message):
    channels_list = ""

    rows = db.select_chats()
    for channel in rows:
        channels_list = channels_list + "ID: " + str(channel[0]) + " | Link: " + str(channel[1]) + "\n"
    await message.reply_text(channels_list)


@Client.on_message(filters.regex("Link chat 🔗") & filters.private & Custom_filters.admin)
async def entery_to_linking_chat(client: Client, message: Message):
    await message.reply_text("Please forward a message from the chat you want to link or /cancel to cancel")
    user_step[message.from_user.id]['step'] = "linking a chat"


@Client.on_message(Custom_filters.linking_channel & filters.private & Custom_filters.admin)
async def linking_chat(client: Client, message: Message):
    del user_step[message.from_user.id]['step']
    chat_id = message.forward_from_chat.id
    timer = True
    try:
        invite_link = await Client.create_chat_invite_link(client, chat_id=chat_id)
    except Exception as e:
        timer = False
        print(e)
        await message.reply_text("Please make robot admin in the chat, bot will automatically try again in a minutes")
        timer = await countdown(60)
        invite_link = await Client.create_chat_invite_link(client, chat_id=chat_id)

    if timer:
        try:
            db.insert_chats(chat_id=chat_id, chat_link=invite_link.invite_link)
            await message.reply_text("The chat successfully unlinked")
        except Exception as e:
            print(e)
            await message.reply_text("An Error Occurred, please try again")


@Client.on_message(filters.regex("Unlink chat ❌") & filters.private & Custom_filters.admin)
async def entery_to_unlinking_chat(client: Client, message: Message):
    await message.reply_text("Please forward a message from the chat you want to unlink or /cancel to cancel")
    user_step[message.from_user.id]['step'] = "unlinking a chat"


@Client.on_message(Custom_filters.unlinking_channel & filters.private & Custom_filters.admin)
async def unlinking_chat(client: Client, message: Message):
    del user_step[message.from_user.id]['step']
    chat_id = message.forward_from_chat.id
    try:
        db.remove_chats(chat_id=chat_id)
        await message.reply_text("The chat successfully unlinked")
    except Exception as e:
        await message.reply_text("An Error Occurred, please try again")
        print(e)
