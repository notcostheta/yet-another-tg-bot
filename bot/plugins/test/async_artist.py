from pyrogram import Client, filters
from pyrogram.errors import MessageTooLong
from pyrogram.types import Message
from pyrogram import enums
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.async_artist_helper import *
from bot.utils.logging import LOGGER
from bot.helpers.filters import dev_cmd


logger = LOGGER(__name__)

try:
    channel = int(CACHE_CHANNEL)  # Important to convert to int
except ValueError:
    logger.error("CACHE_CHANNEL must be a valid integer.")
    channel = None


@Client.on_message(filters.command("artist"))
@ratelimiter
async def artist(client: Client, message: Message):
    if message.text and len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        if message.from_user:
            logger.info(f"Artist: {query} requested by {message.from_user.id}")
        else:
            logger.info(f"Artist: {query} requested.")
        try:
            # Hack that autochecks if the query is a URL
            artist_response = (
                await get_artist_response(query)
                if not await validate_url(query)
                else await get_artist_response_url(query)
            )
            logger.info(f"Artist Response Fetched for {query}")
        except Exception as e:
            logger.error(e)
            await message.reply_text(
                "Something went wrong while fetching the artist. Please try again later."
            )
            return

        # Hack that fixes wrong artist name
        if not artist_response:
            await message.reply_text("Please check the artist name or URL.")
            return

        try:
            # Sends the Image and Caption
            album_response = await get_artist_album_response(artist_response)
            caption = await get_artist_album_caption(artist_response, album_response)
            cover = await get_artist_cover(artist_response)
            send_cover = await message.reply_photo(cover)
        except Exception as e:
            logger.error(e)
            await message.reply_text(
                "Something went wrong while fetching the artist. Please try again later."
            )
            return

        # Short Caption
        if len(caption) > 4096:
            short_caption = await get_short_artist_caption(
                artist_response, album_response
            )
            try:
                await message.reply_text(short_caption, disable_web_page_preview=True)
                if message.from_user:
                    logger.info(
                        f"SHORT CAPTION | Artist: {query} sent to {message.from_user.id}"
                    )
                else:
                    logger.info(f"SHORT CAPTION | Artist: {query} sent.")
                return
            except Exception as e:
                logger.error(e)
                await message.reply_text(
                    "Something went wrong while fetching the artist. Please try again later."
                )
                return

        # Long Caption
        else:
            try:
                send_caption = await message.reply_text(
                    text=caption,
                    disable_web_page_preview=True,
                    reply_to_message_id=send_cover.id,
                )
                if message.from_user:
                    logger.info(
                        f"LONG CAPTION | Artist: {query} sent to {message.from_user.id}"
                    )
                else:
                    logger.info(f"LONG CAPTION | Artist: {query} sent.")
                return
            except Exception as e:
                await message.reply_text(
                    "Something went wrong while fetching the artist. Please try again later."
                )
                logger.error(e)
                return
    else:
        await message.reply_text("Please Provide an Artist.")
        return
