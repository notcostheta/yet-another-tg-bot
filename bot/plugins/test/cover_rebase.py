import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.filters import dev_cmd
from bot.helpers.spot import spotdl
from tqdm import tqdm
import asyncio
from concurrent.futures import ProcessPoolExecutor
from bot.utils.logging import LOGGER

logger = LOGGER(__name__)
executor = ProcessPoolExecutor(max_workers=1)
channel = int(CACHE_CHANNEL)  # Important to convert to int


# Run this function in executor
def get_response(query):
    try:
        response = spotdl.search([query])
        return response
    except Exception as e:
        return str(e)


def get_song_id(response):
    try:
        song_id = response[0].song_id
        return song_id
    except Exception as e:
        return str(e)


def get_album_id(response):
    try:
        album_id = response[0].album_id
        return album_id
    except Exception as e:
        return str(e)


def get_cover_url(response):
    try:
        cover_url = response[0].cover_url
        return cover_url
    except Exception as e:
        return str(e)


def get_album_results(response):
    try:
        id_ = response[0].album_id
        album_url = f"https://open.spotify.com/album/{id_}"
        album = spotdl.search([album_url])
        return album
    except Exception as e:
        return str(e)


def get_song_results(response):
    try:
        song = response[0]
        return song
    except Exception as e:
        return str(e)


@Client.on_message(filters.command("cov") & dev_cmd)
@ratelimiter
async def get_cover(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(" ", 1)[1]
        loop = asyncio.get_event_loop()
        response = await loop.run_in_executor(executor, get_response, query)

        if isinstance(response, str) and response.startswith("Error"):
            await message.reply_text(response)
            return
        else:
            cover_url = await loop.run_in_executor(executor, get_cover_url, response)
            caption = f"""
**Album**: {response[0].album_name}
**Artist**: {response[0].artist}
**Release Date**: {response[0].date}
**Total Tracks**: {response[0].tracks_count}
"""
            await message.reply_photo(cover_url, caption=caption, quote=True)

    else:
        await message.reply_text("Please provide a Song to search for.")


# @Client.on_message(filters.command("cov") & dev_cmd)
# @ratelimiter
# async def get_cover(client: Client, message: Message):
#     if len(message.command) > 1:
#         query = message.text.split(" ", 1)[1]
#         response = await asyncio.to_thread(get_response, query)

#         if isinstance(response, str) and response.startswith("Error"):
#             await message.reply_text(response)
#             return
#         else:
#             cover_url = await asyncio.to_thread(get_cover_url, response)
#             caption = f"""
# **Album**: {response[0].album_name}
# **Artist**: {response[0].artist}
# **Release Date**: {response[0].date}
# **Total Tracks**: {response[0].tracks_count}
# """
#             await message.reply_photo(cover_url, caption=caption, quote=True)

#     else:
#         await message.reply_text("Please provide a Song to search for.")
