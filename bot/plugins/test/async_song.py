from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.async_album_helper import *
from bot.utils.logging import LOGGER
from bot.helpers.filters import dev_cmd

logger = LOGGER(__name__)
channel = int(CACHE_CHANNEL)  # Important to convert to int


@Client.on_message(filters.command("song"))
@ratelimiter
async def album(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(None, 1)[1]

        # Get the song response
        query_response = await get_response(query)
        song = query_response[0]

        # Get the song id and url
        song_id = song.id

        # Get the album response
        metadata, album = await get_album_results(query_response)

        cover = await get_cover_url(query_response)
        send_cover = await message.reply_photo(cover)
        logger.info(
            f"Song: {query} requested by {message.from_user.id}, sending {song_id}."
        )
        return
    else:
        await message.reply_text("Please Provide an Album.")
        return
