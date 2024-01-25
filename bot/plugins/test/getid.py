import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL

channel = int(CACHE_CHANNEL)
@Client.on_message(filters.command("id"))
@ratelimiter
async def get_id(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await message.reply_text(f"Chat ID: `{chat_id}`\nUser ID: `{user_id}`", quote=True)


@Client.on_message(filters.command("upload"))
@ratelimiter
async def upload(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(" ", 1)[1]
        dl = await message.reply_text("Downloading...")
        channel_info = await client.get_chat(channel)
        print(channel_info)
        return
    else:
        await message.reply_text("Provide a valid URL")
