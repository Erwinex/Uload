from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup, ReplyKeyboardRemove
import sqlite3
import Forward_noquote_messages
from Database_code import db
import Custom_filters
from User_step import user_step
from Forward_noquote_messages import ForwardMessages
import hashlib


storage_chat_id = int("-1002222222222") # Fill it with the chat id that you want the bot to save the files in it group, channel or ... channel is perferd.
async def mix_and_hash(str1, str2, length=16):
    # Concatenate the two strings
    combined_str = str1 + str2

    # Create a SHA-256 hash object
    sha256 = hashlib.sha256()

    # Update the hash object with the combined string
    sha256.update(combined_str.encode('utf-8'))

    # Get the hexadecimal representation of the hash
    full_hash = sha256.hexdigest()

    # Truncate the hash to the specified length
    truncated_hash = full_hash[:length]

    return truncated_hash


@Client.on_message(filters.regex("Upload file 📤") & filters.private & Custom_filters.join)
async def upload_handler(client: Client, message: Message):
    await message.reply_text("Send your file as a message or /cancel to cancel", reply_markup=ReplyKeyboardRemove())
    user_step[message.from_user.id]['step'] = "uploading"


@Client.on_message(filters.private & Custom_filters.uploading & Custom_filters.join)
async def is_uploading_handler(client: Client, message: Message):
    del user_step[message.from_user.id]['step']
    try:
        admin_status_up = str(db.select_admin_status(message.from_user.id)).lower()
        bot = await client.get_me()
        if admin_status_up == "admin":
            uploaded = await ForwardMessages.forward_noqoute_messages(
                client,
                chat_id=storage_chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )
            db.insert_files(message_id=str(uploaded.id), chat_id=str(uploaded.chat.id),
                            file_id=await mix_and_hash(str(uploaded.id), str(uploaded.chat.id)))
            await message.reply_text(text="Your file has been uploaded here is your link:\n" +
                                     f"https://t.me/{bot.username}"
                                     f"?start={await mix_and_hash(str(uploaded.id), str(uploaded.chat.id))}",
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
            uploaded = await ForwardMessages.forward_noqoute_messages(
                client,
                chat_id=storage_chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )
            db.insert_files(message_id=str(uploaded.id), chat_id=str(uploaded.chat.id),
                            file_id=await mix_and_hash(str(uploaded.id), str(uploaded.chat.id)))
            await message.reply_text(text="Your file has been uploaded here is your link:\n" +
                                     f"https://t.me/{bot.username}"
                                     f"?start={await mix_and_hash(str(uploaded.id), str(uploaded.chat.id))}",
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
            uploaded = await ForwardMessages.forward_noqoute_messages(
                client,
                chat_id=storage_chat_id,
                from_chat_id=message.chat.id,
                message_ids=message.id
            )
            db.insert_files(message_id=str(uploaded.id), chat_id=str(uploaded.chat.id),
                            file_id=await mix_and_hash(str(uploaded.id), str(uploaded.chat.id)))
            await message.reply_text(text="Your file has been uploaded here is your link:\n" +
                                     f"https://t.me/{bot.username}"
                                     f"?start={await mix_and_hash(str(uploaded.id), str(uploaded.chat.id))}",
                                     reply_markup=ReplyKeyboardMarkup(keyboard=[["Upload file 📤"]], one_time_keyboard=True, resize_keyboard=True))
    except Exception as e:
        print(e)
        await message.reply_text("An Error Occurred, please try again")


# Admins accessibilities


@Client.on_message(filters.regex("Delete file 🗑") & filters.private & Custom_filters.admin)
async def delete_handler(client: Client, message: Message):
    await message.reply_text("Send the link of the file that you want to remove or /cancel to cancel")
    user_step[message.from_user.id]['step'] = "deleting file"


@Client.on_message(Custom_filters.deleting_file & filters.private & Custom_filters.admin)
async def is_deleting_handler(client: Client, message: Message):
    del user_step[message.from_user.id]['step']
    file_id = message.text.split("=")[1]
    print(file_id)
    try:
        db.remove_file(file_id)
        await message.reply_text("The file has been successfully deleted")
    except Exception as e:
        print(e)
        await message.reply_text("An Error Occurred")


@Client.on_message(filters.regex("File status 📊") & filters.private & Custom_filters.admin)
async def file_status_handler(client: Client, message: Message):
    await message.reply_text("Send the link of the file that you want to get its status or /cancel to cancel")
    user_step[message.from_user.id]['step'] = "getting file status"


@Client.on_message(Custom_filters.getting_file_status & filters.private & Custom_filters.admin)
async def handling_file_status(client: Client, message: Message):
    del user_step[message.from_user.id]['step']
    file_id = message.text.split("=")[1]
    try:
        downloads = db.select_files_downloads(file_id)
        await message.reply_text(f"Your file downloaded {downloads} times")
    except Exception as e:
        print(e)
        await message.reply_text("An Error Occurred")


@Client.on_message(filters.regex("Users count 👥") & filters.private & Custom_filters.admin)
async def users_count_handler(client: Client, message: Message):
    users_count = db.users_count()
    await message.reply_text(f"We have {str(users_count)} active user")


@Client.on_message(filters.regex("Global message 📣") & filters.private & Custom_filters.admin)
async def global_message_handler(client: Client, message: Message):
    user_step[message.from_user.id]["step"] = "sending global message"
    await message.reply_text("Send us the message to send to all users or /cancel to cancel")


@Client.on_message(Custom_filters.global_message & filters.private & Custom_filters.admin)
async def is_handling_global_message(client: Client, message: Message):
    del user_step[message.from_user.id]["step"]
    users = db.select_users()
    done = True
    for user in users:
        try:
            await ForwardMessages.forward_noqoute_messages(
                client,
                chat_id=int(user[0]),
                from_chat_id=message.chat.id,
                message_ids=message.id
            )
        except Exception as e:
            print("An Error Occurred | " + str(e))
            done = False
    if done:
        await message.reply_text("Message successfully sent to all users")
    else:
        await message.reply_text("An Error Occurred, please try again")

# Owner accessibilities


@Client.on_message(filters.regex("Admins list 👤") & filters.private & Custom_filters.admin)
async def admins_list_handler(client: Client, message: Message):
    admin_status = str(db.select_admin_status(message.from_user.id)).lower()

    if admin_status == "owner":
        admins_list = "1"
        try:
            rows = db.admins_list()
            for admin in rows:
                admins_list = admins_list + "ID: " + str(admin[0]) + " | rule: " + str(admin[1]) + "\n"
                print(admin)
        except Exception as e:
            print(e)
        await message.reply_text(admins_list)
    else:
        await message.reply_text("Access denied ⚠️")


@Client.on_message(filters.regex("Add admin 🧑‍💻") & filters.private & Custom_filters.admin)
async def add_admin_handler(client: Client, message: Message):
    admin_status = str(db.select_admin_status(message.from_user.id)).lower()
    if admin_status == "owner":
        await message.reply_text("Please send the user ID to make admin or /cancel to cancel")
        user_step[message.from_user.id]['step'] = "add admin"
    else:
        await message.reply_text("Access denied ⚠️")


@Client.on_message(Custom_filters.adding_admin & filters.private & Custom_filters.admin)
async def adding_admin_handler(client: Client, message: Message):
    del user_step[message.from_user.id]['step']
    try:
        is_success = db.add_admin(str(int(message.text)))
        if is_success:
            await message.reply_text("New admin added successfully")
        else:
            await message.reply_text("This operation is not allowed")
    except Exception as e:
        print(e)
        await message.reply_text("An Error Occurred, please check the ID")


@Client.on_message(filters.regex("Remove admin 🚫") & filters.private & Custom_filters.admin)
async def remove_admin_handler(client: Client, message: Message):
    admin_status = str(db.select_admin_status(message.from_user.id)).lower()
    if admin_status == "owner":
        await message.reply_text("Please send the admin ID to remove or /cancel to cancel")
        user_step[message.from_user.id]['step'] = "remove admin"
    else:
        await message.reply_text("Access denied ⚠️")


@Client.on_message(Custom_filters.removing_admin & filters.private & Custom_filters.admin)
async def removing_admin_handler(client: Client, message: Message):
    del user_step[message.from_user.id]['step']
    try:
        is_success = db.remove_admin(message.text)
        if is_success:
            await message.reply_text("The admin successfully removed")
        else:
            await message.reply_text("This operation is not allowed")
    except Exception as e:
        print(e)
        await message.reply_text("An Error Occurred, please check the ID")

