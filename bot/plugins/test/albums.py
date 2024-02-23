from pyrogram import Client, filters
from pyrogram.types import Message
from tqdm import tqdm

from bot.helpers.decorators import ratelimiter
from bot.helpers.spot import spotdl

import asyncio
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=1)


def get_album_id(url):
    try:
        search = spotdl.search([url])
        album = search[0].album_id
        album_url = f"https://open.spotify.com/album/{album}"
        return album_url
    except Exception as e:
        return str(e)


def download_album(album_url):
    try:
        search = spotdl.search([album_url])
        results = []
        for song in search:
            song, path = spotdl.download(song)
            results.append(path)
        return results
    except Exception as e:
        return str(e)


async def progress(current, total):
    if not hasattr(progress, "pbar"):
        progress.pbar = tqdm(total=total, ncols=70, unit="B", unit_scale=True)
    progress.pbar.update(current - progress.pbar.n)


async def send_album(message: Message, url: str):
    loop = asyncio.get_event_loop()
    album_url = await loop.run_in_executor(executor, get_album_id, url)
    print(album_url)
    paths = await loop.run_in_executor(executor, download_album, album_url)

    if isinstance(paths, str) and paths.startswith("Error"):
        await message.reply_text(paths)
        return None
    else:
        file_ids = []
        for path in paths:
            sent_message = await message.reply_audio(
                audio=path, quote=False, progress=progress
            )
            file_ids.append(sent_message.audio.file_id)
        progress.pbar.close()
        return file_ids


@Client.on_message(filters.command(["album_123"]) & filters.private)
@ratelimiter
async def song(_, message: Message):
    if len(message.command) > 1:
        query = message.text.split(" ", 1)[1]
        dl = await message.reply_text("Downloading...")
        
        cached_ids = await send_album(message, query)
        print(cached_ids)
    else:
        await message.reply_text("No Song Provided!", quote=True)
