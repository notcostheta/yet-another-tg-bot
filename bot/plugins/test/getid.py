import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL

channel = int(CACHE_CHANNEL)  # Important to convert to int


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

        req = await client.send_message(
            chat_id=channel,
            text=f"{query} requested by {message.from_user.mention}",
            disable_notification=True,
        )

        audio_path = "content/Catalyst... - Nice to see you.mp3"
        file = await client.send_audio(
            chat_id=channel,
            audio=audio_path,
        )

        file_id = file.audio.file_id
        send = await client.send_cached_media(chat_id=message.chat.id, file_id=file_id)
        
        return
    else:
        await message.reply_text("Provide a valid URL")
