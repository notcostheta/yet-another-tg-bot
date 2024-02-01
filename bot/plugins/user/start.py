from pyrogram import Client, filters
from pyrogram.types import Message

from bot.helpers.filters import valid_users
from bot.database.database import save_user
from bot.helpers.decorators import ratelimiter


@Client.on_message(filters.command(["start"]) & filters.private)
@ratelimiter
async def start(_, message: Message):
    user = message.from_user
    await save_user(message.from_user)
    await message.reply_text(
        f"Welcome aboard! {user.first_name}! 🎉\n\n"
        f"You're being saved in my database with the ID: `{user.id}`. "
    )
    await message.reply_text(
        text="Hi, I'm a bot that can download songs from Spotify and send them to you. Send /song <song link> to download a song.",
        quote=False,
    )
