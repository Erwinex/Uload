from pyrogram import filters, Client
from pyrogram.types import Message
import sqlite3
from Database_code import db

plugins_dir = dict(
    root="plugins"
)

app = Client(name="Uload", # You can change it if you'd like to
             api_id= int(), # Replace it with your own one
             api_hash="", # Replace it with your own one
             plugins=plugins_dir,
             bot_token="" # Replace it with your own one
             )

app.run()

db.close_db()
