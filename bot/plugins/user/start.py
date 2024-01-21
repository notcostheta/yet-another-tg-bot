from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers.decorators import ratelimiter


@Client.on_message(filters.command(["start"]) & filters.private)
@ratelimiter
async def start(_, message: Message):
    await message.reply_text(
        text="Hi, I'm a bot that can download songs from Spotify and send them to you. Send /song <song link> to download a song.",
        quote=True,
    )
