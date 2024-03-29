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


@Client.on_message(filters.command("album1"))
@ratelimiter
async def album(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        logger.info(f"Album: {query} requested by {message.from_user.id}")

        # Get the query response
        query_response = await get_response(query)
        metadata, album = await get_album_results(query_response)

        long_caption = await get_caption(metadata, album)

        if len(long_caption) > 4096:
            try:
                short_caption = await get_short_caption(metadata, album)
                await message.reply_text(short_caption)
                logger.info(
                    f"SHORT CAPTION | Album: {query} sent to {message.from_user.id}"
                )
                return
            except Exception as e:
                logger.error(e)
                await message.reply_text(
                    "Something went wrong while fetching the album. Please try again later."
                )
                return
        else:
            try:
                cover_url = await get_cover_url(query_response)
                send_cover = await message.reply_photo(cover_url)
                await message.reply_text(
                    text=long_caption,
                    reply_to_message_id=send_cover.id,
                    disable_web_page_preview=True,
                )
                logger.info(
                    f"LONG CAPTION | Album: {query} sent to {message.from_user.id}"
                )
            except Exception as e:
                logger.error(e)
                await message.reply_text(
                    "Something went wrong while fetching the album. Please try again later."
                )
        return
    else:
        await message.reply_text("Please Provide an Album.")
        return
