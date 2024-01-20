from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers.decorators import ratelimiter


@Client.on_message(filters.command(["song"]) & filters.private)
@ratelimiter
async def song(_, message: Message):
    if len(message.command) > 1:
        url = message.text.split(" ", 1)[1]
        await message.reply_text(url, quote=True)
    else:
        await message.reply_text("No Song Provided!", quote=True)
