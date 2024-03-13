from pyrogram import filters, Client
from pyrogram.types import Message, ReplyKeyboardMarkup,  InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ReplyKeyboardRemove
import sqlite3
from Database_code import db
from Forward_noquote_messages import ForwardMessages
import Custom_filters
import time
import asyncio
from User_step import user_step

# how many seconds do you want take to delete the message
auto_delete_afterS = 60
# timer for automatically deleting


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


# Example usage in an asynchronous context

async def countdown(seconds):
    for i in range(seconds, 0, -1):
        await asyncio.sleep(1)
    return True


print("starting")


@Client.on_message(filters.command("start") & filters.private & ~ Custom_filters.downloading)
async def start_handler(client: Client, message: Message):
    try:
        db.insert_users(message.from_user.id)
        pass
    except Exception as e:
        print(str(e))
        pass

    admin_status = str(db.select_admin_status(message.from_user.id)).lower()
    if admin_status == "none":
        await message.reply_text("Hi welcome to our uploader bot",
                                 reply_markup=ReplyKeyboardMarkup(keyboard=[["Upload file 📤"]], resize_keyboard=True))
    elif admin_status == "admin":
        await message.reply_text("Hi dear admin welcome to your uploader bot",
                                 reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True,
                                     resize_keyboard=True,
                                     keyboard=[
                                         ["Upload file 📤", "Delete file 🗑", "File status 📊"],
                                         ["Chats list 📢", "Link chat 🔗", "Unlink chat ❌"],
                                         ["Users count 👥", "Global message 📣"]
                                     ]
                                 )
                                 )
    elif admin_status == "owner":
        await message.reply_text("Hi dear owner welcome to your uploader bot",
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
    else:
        print(admin_status)


@Client.on_message(filters.command("start") & filters.private & Custom_filters.downloading & Custom_filters.join)
async def download_handler(client: Client, message: Message):
    try:
        db.insert_users(message.from_user.id)
        pass
    except Exception as e:
        print(e)
        pass

    admin_status = str(db.select_admin_status(message.from_user.id)).lower()
    try:
        the_file_id = message.text.split(" ")[1]
        file_data = db.select_files_data(the_file_id)
        sended_message = await ForwardMessages.forward_noqoute_messages(
            client,
            chat_id=message.chat.id,
            from_chat_id=int(file_data[1]),
            message_ids=int(file_data[0])
        )
        db.update_files_downloads(the_file_id)
        if admin_status == "none":
            await message.reply_text("Here is your file save it in your saved messages"
                                     f" it will be automatically deleted in {auto_delete_afterS} seconds",
                                     reply_markup=ReplyKeyboardMarkup(keyboard=[["Upload file 📤"]], one_time_keyboard=True, resize_keyboard=True))
        elif admin_status == "admin":
            await message.reply_text("Here is your file save it in your saved messages"
                                     f" it will be automatically deleted in {auto_delete_afterS} seconds",
                                     reply_markup=ReplyKeyboardMarkup(
                                         resize_keyboard=True,
                                         keyboard=[
                                             ["Upload file 📤", "Delete file 🗑", "File status 📊"],
                                             ["Chats list 📢", "Link chat 🔗", "Unlink chat ❌"],
                                             ["Users count 👥", "Global message 📣"]
                                         ]
                                     )
                                     )
        elif admin_status == "owner":
            await message.reply_text("Here is your file save it in your saved messages"
                                     f" it will be automatically deleted in {auto_delete_afterS} seconds",
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
        else:
            print(admin_status)
        timer = await countdown(auto_delete_afterS)
        if timer:
            await sended_message.delete(revoke=True)

    except Exception as e:
        print(e)
        await message.reply_text("Something went wrong")


async def int_to_ordinal(number):
    await asyncio.sleep(1)  # Simulating an asynchronous operation (you can replace this with actual async code)

    if 10 <= number % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(number % 10, 'th')

    return str(number) + suffix


@Client.on_callback_query()
async def recheck_join(client: Client, callback_query: CallbackQuery):
    print(callback_query.data)
    try:
        check_file_id = callback_query.data.split("=")[1]

    except:
        check_file_id = None

    if (callback_query.data == "check join upload" or
            callback_query.data == f"check join download file ID ={check_file_id}"):
        rows = db.select_chats()
        buttons = []
        i = 0
        joined = True
        for channel in rows:
            await client.get_chat(channel[0])
            try:
                i += 1
                chat_memeber = await client.get_chat_member(chat_id=int(channel[0]),user_id=callback_query.from_user.id)
            except Exception as e:
                joined = False
                buttons.append([InlineKeyboardButton(text=f"sponsor {await get_emoji(i)}",
                                                     url=channel[1])])  # {int_to_ordinal(i)}
                print(e)
        if not joined:
            # inline markup needed
            if callback_query.data == "check join upload":
                buttons.append([InlineKeyboardButton(text="I've joined to the sponsors",
                                                     callback_data="check join upload")])
            else:
                buttons.append([InlineKeyboardButton(
                    text="I've joined to the sponsors",
                    callback_data=f"check join download file ID ={callback_query.data.split('=')[1]}")])
            await CallbackQuery.edit_message_text(self=callback_query,
                                                  text="You need to join to all our sponsors for using robot ❗️",
                                                  reply_markup=InlineKeyboardMarkup(buttons))
            return False
        else:
            #print(callback_query.message)
            if callback_query.data == "check join upload":
                await callback_query.message.reply_text("Send your file as a message or /cancel to cancel",
                                                        reply_markup=ReplyKeyboardRemove())
                user_step[callback_query.message.from_user.id]['step'] = "uploading"
                await callback_query.message.delete(revoke=True)
            else:
                admin_status = str(db.select_admin_status(callback_query.from_user.id)).lower()
                try:
                    the_file_id = callback_query.data.split("=")[1]
                    file_data = db.select_files_data(the_file_id)
                    sended_message = await ForwardMessages.forward_noqoute_messages(
                        client,
                        chat_id=callback_query.message.chat.id,
                        from_chat_id=int(file_data[1]),
                        message_ids=int(file_data[0])
                    )
                    db.update_files_downloads(the_file_id)
                    if admin_status == "none":
                        await callback_query.message.reply_text("Here is your file save it in your saved messages"
                                                 f" it will be automatically deleted in {auto_delete_afterS} seconds",
                                                 reply_markup=ReplyKeyboardMarkup(keyboard=[["Upload file 📤"]], one_time_keyboard=True, resize_keyboard=True))
                        await callback_query.message.delete(revoke=True)
                    elif admin_status == "admin":
                        await callback_query.message.reply_text("Here is your file save it in your saved messages"
                                                 f" it will be automatically deleted in {auto_delete_afterS} seconds",
                                                 reply_markup=ReplyKeyboardMarkup(one_time_keyboard=True,
                                                     resize_keyboard=True,
                                                     keyboard=[
                                                         ["Upload file 📤", "Delete file 🗑", "File status 📊"],
                                                         ["Chats list 📢", "Link chat 🔗", "Unlink chat ❌"],
                                                         ["Users count 👥", "Global message 📣"]
                                                     ]
                                                 )
                                                 )
                        await callback_query.message.delete(revoke=True)
                    elif admin_status == "owner":
                        await callback_query.message.reply_text("Here is your file save it in your saved messages"
                                                 f" it will be automatically deleted in {auto_delete_afterS} seconds",
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
                        await callback_query.message.delete(revoke=True)
                    else:
                        print(admin_status)
                    timer = await countdown(auto_delete_afterS)
                    if timer:
                        await sended_message.delete(revoke=True)
                except Exception as e:
                    print(e)
                    await callback_query.message.reply_text("Something went wrong")
                return True
