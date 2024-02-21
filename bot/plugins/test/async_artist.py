from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import enums
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.async_artist import *
from bot.utils.logging import LOGGER
from bot.helpers.filters import dev_cmd

logger = LOGGER(__name__)
channel = int(CACHE_CHANNEL)  # Important to convert to int


@Client.on_message(filters.command("artist"))
@ratelimiter
async def artist(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        
        # Hack that autochecks if the query is a URL
        artist_response = (
            await get_artist_response(query)
            if not await validate_url(query)
            else await get_artist_response_url(query)
        )
        
        # Hack that fixes wrong artist name
        if not artist_response:
            await message.reply_text("Please check the artist name or URL.")
            return

        # Sends the Image and Caption
        album_response = await get_artist_album_response(artist_response)
        caption = await get_artist_album_caption(artist_response, album_response)
        cover = await get_artist_cover(artist_response)
        send_cover = await message.reply_photo(cover)
        send_caption = await message.reply_text(
            text=caption,
            disable_web_page_preview=True,
            parse_mode=enums.ParseMode.MARKDOWN,
            reply_to_message_id=send_cover.id,
        )
        logger.info(f"Artist: {query} requested by {message.from_user.id}")
        return
    else:
        await message.reply_text("Please Provide an Artist.")
        return
