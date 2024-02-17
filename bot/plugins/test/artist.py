import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.filters import dev_cmd
from bot.helpers.spot import spotdl, spotify
from tqdm import tqdm
import asyncio
from concurrent.futures import ProcessPoolExecutor
from bot.utils.logging import LOGGER
from pyrogram import enums

logger = LOGGER(__name__)
executor = ProcessPoolExecutor(max_workers=1)
channel = int(CACHE_CHANNEL)  # Important to convert to int


async def get_response(name: str) -> dict:
    try:
        results = spotify.search(q="artist:" + name, type="artist")
        if not results["artists"]["items"]:
            return {}
        return results
    except Exception as e:
        return {"error": str(e)}


async def get_artist_caption(results: dict) -> str:
    if not results:
        return None
    else:
        artist = results["artists"]["items"][0]
        artist_id = artist["id"]

        results = spotify.artist_albums(
            artist_id, album_type="compilation,album,single", limit=50
        )
        albums = results["items"]
        albums.sort(key=lambda x: x["release_date"], reverse=True)
        formatted_albums = [
            f"[{album['name']}]({album['external_urls']['spotify']})"
            for album in albums
        ]
        caption_header = f"""**Artist**: [{artist['name']}](https://open.spotify.com/artist/{artist['id']})
**Genres**: {", ".join(artist['genres'])}
**Followers**: {artist['followers']['total']}
**Discography**:
"""
        albums_string = "\n".join(formatted_albums)
        caption = caption_header + albums_string
        return caption


async def get_artist_cover(results: dict) -> str:
    if not results:
        return None
    else:
        artist = results["artists"]["items"][0]
        return artist["images"][0]["url"]


async def get_album_list(results: dict) -> list:
    if not results:
        return None
    else:
        artist = results["artists"]["items"][0]
        artist_id = artist["id"]
        results = spotify.artist_albums(artist_id, album_type="album")
        albums = results["items"]
        albums.sort(key=lambda x: x["release_date"], reverse=True)
        albums = [album["external_urls"]["spotify"] for album in albums]
        return albums


@Client.on_message(filters.command("artist") & dev_cmd)
@ratelimiter
async def artist(client: Client, message: Message):
    if len(message.command) > 1:
        query = message.text.split(None, 1)[1]
        response = await get_response(query)
        if not response:
            await message.reply_text(f"No results found for {query}.")
            return
        else:
            caption = await get_artist_caption(response)
            cover = await get_artist_cover(response)
            albums = await get_album_list(response)

            send_cover = await message.reply_photo(cover)
            send_caption = await message.reply_text(
                text=caption,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.MARKDOWN,
                reply_to_message_id=send_cover.id,
            )
    else:
        await message.reply_text("Please provide an artist name.")
