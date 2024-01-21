from pyrogram import Client, filters
from pyrogram.types import Message
from tqdm import tqdm

from bot.helpers.decorators import ratelimiter
from bot.helpers.spot import spotdl

import asyncio
from concurrent.futures import ProcessPoolExecutor

executor = ProcessPoolExecutor(max_workers=1)

def download_song(url):
    try:
        search = spotdl.search([url])
        song, path = spotdl.download(search[0])
        return path
    except Exception as e:
        return str(e)

async def progress(current, total):
    if not hasattr(progress, "pbar"):
        progress.pbar = tqdm(total=total, ncols=70, unit='B', unit_scale=True)
    progress.pbar.update(current - progress.pbar.n)

async def download_and_send_song(message: Message, url: str):
    loop = asyncio.get_event_loop()
    path = await loop.run_in_executor(executor, download_song, url)

    if isinstance(path, str) and path.startswith("Error"):
        await message.reply_text(path)
    else:
        await message.reply_audio(audio=path, quote=True, progress=progress)
        progress.pbar.close()

@Client.on_message(filters.command(["song"]) & filters.private)
@ratelimiter
async def song(_, message: Message):
    if len(message.command) > 1:
        url = message.text.split(" ", 1)[1]
        await message.reply_text("Downloading...")
        await download_and_send_song(message, url)
    else:
        await message.reply_text("No Song Provided!", quote=True)