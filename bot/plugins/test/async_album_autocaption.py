from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.async_album_helper import *
from bot.utils.logging import LOGGER
from bot.helpers.filters import dev_cmd
from bot.helpers.telegraph_helper import telegraph_paste

logger = LOGGER(__name__)
channel = int(CACHE_CHANNEL)  # Important to convert to int


@Client.on_message(filters.command("album"))
@ratelimiter
async def album(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        logger.info(f"Album: {query} requested by {message.from_user.id}")

        # Get the query response
        query_response = await get_response(query)
        metadata, album = await get_album_results(query_response)

        # Get the cover and caption
        cover_url = await get_cover_url(query_response)
        caption = await autocaption(metadata, album)

        # Send the cover and caption to the user
        sent_cover = await message.reply_photo(cover_url)
        await message.reply_text(
            text=caption,
            reply_to_message_id=sent_cover.id,
            disable_web_page_preview=True,
        )
        logger.info(f"Album: {query} sent to {message.from_user.id}")
        return
    else:
        await message.reply_text("Please provide an album name to search for.")
        return
