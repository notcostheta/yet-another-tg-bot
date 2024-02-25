from pyrogram import Client, filters
from pyrogram.types import Message
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.async_playlist_helper import *
from bot.utils.logging import LOGGER
from bot.helpers.filters import dev_cmd


logger = LOGGER(__name__)


@Client.on_message(filters.command("playlist"))
@ratelimiter
async def playlist(client: Client, message: Message):
    if message.text and len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        if message.from_user:
            logger.info(f"Playlist: {query} requested by {message.from_user.id}")
        else:
            logger.info(f"Playlist: {query} requested.")
        try:
            # Hack that autochecks if the query is a URL
            playlist_response = await get_response(query)
            logger.info(f"Playlist Response Fetched for {query}")
        except Exception as e:
            logger.error(e)
            await message.reply_text(
                "Something went wrong while fetching the playlist. Please try again later."
            )
            return

        # Hack that fixes wrong playlist name
        if not playlist_response:
            await message.reply_text("Please check the playlist name or URL.")
            return

        try:
            # Sends the Image and Caption
            caption = await get_caption(playlist_response[0], playlist_response[1])
            cover = await get_cover_url(playlist_response[0])
            send_cover = await message.reply_photo(photo=cover, caption=caption)
            logger.info(f"Playlist Sent for {query}")
            return
        except Exception as e:
            logger.error(e)
            await message.reply_text(
                "Something went wrong while fetching the playlist. Please try again later."
            )
            return
    else:
        await message.reply_text("Please provide a query to search for.")
        return
