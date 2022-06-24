from pyrogram import Client
from telethon import TelegramClient
import os


# TG_APP_ID= os.environ.get("TG_APP_ID")

# TG_API_HASH=os.environ.get("TG_API_HASH")
TG_APP_ID= os.environ.get("TG_APP_ID")

TG_API_HASH=os.environ.get("TG_API_HASH")

bot_token="5426263444:AAG_YopkxFE3g5UBM7PHVUSZogVqUL-yLEc"
# bot_token=""
bot=Client("Refer", 
           
    api_id=8619734,
    api_hash="659edfec11b95410a10d5e2d917bd98a",
         #   bot_token='5426263444:AAG_YopkxFE3g5UBM7PHVUSZogVqUL-yLEc')
           bot_token='5426263444:AAG_YopkxFE3g5UBM7PHVUSZogVqUL-yLEc')




bot2 = TelegramClient(
           "Telethon Helper",
    api_id=8619734,
    api_hash="659edfec11b95410a10d5e2d917bd98a",
).start(bot_token=bot_token)
