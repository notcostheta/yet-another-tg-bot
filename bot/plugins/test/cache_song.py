from pyrogram import Client, filters
from pyrogram.types import Message
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.async_album_helper import *
from bot.utils.logging import LOGGER
from bot.helpers.filters import dev_cmd
from bot.database.database import save_album
from concurrent.futures import ProcessPoolExecutor
import asyncio
import pathlib
from rich import print


logger = LOGGER(__name__)
channel = int(CACHE_CHANNEL)  # Important to convert to int
executor = ProcessPoolExecutor(max_workers=1)


@Client.on_message(filters.command("song"))
@ratelimiter
async def song(client: Client, message: Message):
    if message.text and len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        if message.from_user:
            logger.info(f"Song: {query} requested by {message.from_user.id}")
        else:
            logger.info(f"Song: {query} requested but no user found.")
        try:
            # Get the song response
            query_response = await get_response(query)
            song = query_response[0]
            logger.info(f"Song Response Fetched for {query}")
        except Exception as e:
            logger.error(e)
            await message.reply_text(
                "Something went wrong while fetching the song. Please try again later."
            )
            return

        # Get the song_id and album_id
        song_id = song.song_id
        album_id = song.album_id
        # Get the album results
        album_results = await get_album_results(query_response)
        metadata = album_results[0]
        album = album_results[1]

        # Get the loop
        loop = asyncio.get_event_loop()
        results = await loop.run_in_executor(executor, download_album, album)
        paths = [result[1] for result in results]
        print(paths)

        # Send cover and caption to the channel
        cover = await get_cover_url(query_response)
        caption = await get_caption(metadata, album)
        sent_cover = client.send_photo(channel, cover)
        sent_caption = client.send_message(
            chat_id=channel,
            text=caption,
            disable_web_page_preview=True,
            parse_mode="markdown",
            reply_to_message_id=sent_cover.message_id,
        )

        # Send paths to the channel
        for path in paths:
            file_ids = []
            cached_audio = await client.send_audio(channel, audio=path)
            file_ids.append(cached_audio.audio.file_id)

        # Send the song to the user
        