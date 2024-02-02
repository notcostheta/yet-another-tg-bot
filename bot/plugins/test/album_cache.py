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


@Client.on_message(filters.command("id") & dev_cmd)
@ratelimiter
async def get_id(client: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    await message.reply_text(f"Chat ID: `{chat_id}`\nUser ID: `{user_id}`", quote=True)


def get_album_id(query):
    try:
        search = spotdl.search([query])
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


async def cache_album(client: Client, message: Message, url: str):
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
            cached_audio = await client.send_audio(
                chat_id=channel,
                audio=path,
                progress=progress,
            )
            file_ids.append(cached_audio.audio.file_id)
        progress.pbar.close()
        return file_ids


@Client.on_message(filters.command("upload"))
@ratelimiter
async def upload(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(" ", 1)[1]
        dl = await message.reply_text("Downloading...")

        req = await client.send_message(
            chat_id=channel,
            text=f"{query} requested by {message.from_user.mention}",
            disable_notification=True,
        )

        audio_path = await cache_album(client, message, query)

        if audio_path is None:
            await dl.edit_text("Error downloading song")
            logger.error(f"Error downloading {query}")
            return
        else:
            for path in audio_path:
                await client.send_cached_media(
                    chat_id=message.chat.id,
                    file_id=path,
                )
            logger.info(f"Uploaded {query}")
            await dl.edit_text("Uploaded")
            return

    else:
        await message.reply_text("Provide a valid URL")
