from pyrogram import filters, Client
from pyrogram.types import Message,  InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardMarkup
import sqlite3
from Database_code import db
from User_step import user_step
import re
import asyncio

# check if is admin or not


async def admin_filter(_, client: Client, message: Message):
    admin_status = str(db.select_admin_status(message.from_user.id)).lower()
    if admin_status == "admin" or admin_status == "owner":
        return True
    else:
        await message.reply_text("Access denied ⚠️")
        return False

admin = filters.create(admin_filter)


async def is_uploading(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "uploading" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "uploading" and message.text == "/cancel":
        try:
            admin_status_up = str(db.select_admin_status(message.from_user.id)).lower()
            bot = await client.get_me()
            if admin_status_up == "admin":
                await message.reply_text(text="Successfully canceled 📛",
                                         reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True,
                                             keyboard=[
                                                 ["Upload file 📤", "Delete file 🗑", "File status 📊"],
                                                 ["Chats list 📢", "Link chat 🔗", "Unlink chat ❌"],
                                                 ["Users count 👥", "Global message 📣"]
                                             ]
                                         )
                                         )

            elif admin_status_up == "owner":
                await message.reply_text(text="Successfully canceled 📛",
                                         reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True,
                                             resize_keyboard=True,
                                             keyboard=[
                                                 ["Upload file 📤", "Delete file 🗑", "File status 📊"],
                                                 ["Chats list 📢", "Link chat 🔗", "Unlink chat ❌"],
                                                 ["Admins list 👤", "Add admin 🧑‍💻", "Remove admin 🚫"],
                                                 ["Users count 👥", "Global message 📣"]
                                             ]
                                         )
                                         )

            elif admin_status_up == "none":
                await message.reply_text(text="Successfully canceled 📛",
                                         reply_markup=ReplyKeyboardMarkup(keyboard=[["Upload file 📤"]], one_time_keyboard=True, resize_keyboard=True))
        except Exception as e:
            print(e)
    else:
        return False

uploading = filters.create(is_uploading)


async def is_downloading(_, client: Client, message: Message):
    if len(message.text) >= 7:
        return True
    else:
        return False

downloading = filters.create(is_downloading)


async def int_to_ordinal(number):
    await asyncio.sleep(1)  # Simulating an asynchronous operation (you can replace this with actual async code)

    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

    return str(number) + suffix


async def get_emoji(number):
    try:
        # Convert the number to an integer
        number = int(number)

        # Define a mapping of numbers to emojis
        emoji_mapping = {
            0: '0️⃣',
            1: '🥇',
            2: '🥈',
            3: '🥉',
            4: '4️⃣',
            5: '5️⃣',
            6: '6️⃣',
            7: '7️⃣',
            8: '8️⃣',
            9: '9️⃣',
            10: '🔟',
        }

        # Check if the number is in the mapping
        if 0 <= number <= 10:
            return emoji_mapping[number]
        else:
            print("Number out of range. Please choose a number between 0 and 10.")
    except ValueError:
        print("Invalid input. Please provide a valid number.")


async def join_ckecker(_, client: Client, message: Message):
    rows = db.select_chats()
    buttons = []
    i = 0
    joined = True
    for channel in rows:
        try:
            i += 1
            chat_memeber = await client.get_chat_member(chat_id=str(int(channel[0])), user_id=message.from_user.id)
        except Exception as e:
            joined = False
            buttons.append([InlineKeyboardButton(text=f"sponsor {await get_emoji(i)}", url=channel[1])]) # {await int_to_ordinal(i)}
            print(e)
    if not joined:
        # inline markup needed
        if message.text == "Upload file 📤":
            buttons.append([InlineKeyboardButton(text="I've joined to the sponsors",
                                                 callback_data="check join upload")])
        else:
            buttons.append([InlineKeyboardButton(
                text="I've joined to the sponsors",
                callback_data=f"check join download file ID ={message.text.split(' ')[1]}")])
        await message.reply_text("You need to join to our sponsors for using robot ⭕️",
                                 reply_markup=InlineKeyboardMarkup(buttons))
        return False
    else:
        return True

join = filters.create(join_ckecker)


async def is_linking_channel(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "linking a chat" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "linking a chat" and message.text == "/cancel":
        del user_step[message.from_user.id]["step"]
        await message.reply_text("Successfully canceled 📛")
    else:
        return False

linking_channel = filters.create(is_linking_channel)


async def is_unlinking_channel(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "unlinking a chat" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "unlinking a chat" and message.text == "/cancel":
        del user_step[message.from_user.id]["step"]
        await message.reply_text("Successfully canceled 📛")
    else:
        return False

unlinking_channel = filters.create(is_unlinking_channel)


async def is_deleting_file(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "deleting file" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "deleting file" and message.text == "/cancel":
        del user_step[message.from_user.id]["step"]
        await message.reply_text("Successfully canceled 📛")
    else:
        return False

deleting_file = filters.create(is_deleting_file)


async def is_getting_file_status(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "getting file status" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "getting file status" and message.text == "/cancel":
        del user_step[message.from_user.id]["step"]
        await message.reply_text("Successfully canceled 📛")
    else:
        return False

getting_file_status = filters.create(is_getting_file_status)


async def is_sending_global_message(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "sending global message" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "sending global message" and message.text == "/cancel":
        del user_step[message.from_user.id]["step"]
        await message.reply_text("Successfully canceled 📛")
    else:
        return False

global_message = filters.create(is_sending_global_message)


async def is_adding_admin(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "add admin" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "add admin" and message.text == "/cancel":
        del user_step[message.from_user.id]["step"]
        await message.reply_text("Successfully canceled 📛")
    else:
        return False

adding_admin = filters.create(is_adding_admin)


async def is_removing_admin(_, client: Client, message: Message):
    if user_step[message.from_user.id]["step"] == "remove admin" and message.text != "/cancel":
        return True
    elif user_step[message.from_user.id]["step"] == "remove admin" and message.text == "/cancel":
        del user_step[message.from_user.id]["step"]
        await message.reply_text("Successfully canceled 📛")
    else:
        return False

removing_admin = filters.create(is_removing_admin)
