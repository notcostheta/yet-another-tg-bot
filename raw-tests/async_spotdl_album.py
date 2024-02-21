import asyncio
from spotdl import Spotdl
from spotdl.types.song import SongList
from spotdl.types.album import Album
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from rich import print

spotdl = Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    downloader_settings={"output": "content"},
)


async def get_response(query: str) -> SongList:
    try:
        response = spotdl.search([query])
        return response
    except Exception as e:
        return [(e)]


async def get_album_results(response: SongList) -> SongList:
    try:
        id_ = response[0].album_id
        album_url = f"https://open.spotify.com/album/{id_}"
        album = spotdl.search([album_url])
        album = sorted(album, key=lambda song: song.track_number)
        return album
    except Exception as e:
        return [(e)]


async def get_cover_url(response: SongList) -> str:
    try:
        cover_url = response[0].cover_url
        return cover_url
    except Exception as e:
        return [(e)]


async def get_caption(album: SongList) -> str:
    try:
        caption_header = f"""**Album**: {album[0].album_name}
**Artists**: {album[0].album_artist}
**Release Date**: {album[0].date}
**Total Tracks**: {album[0].tracks_count}
"""
        tracks_str = "\n".join([f"[{track.name}]({track.url})" for track in album])
        caption = f"{caption_header}\n**Tracks**:\n{tracks_str}"
        return caption
    except Exception as e:
        return str(e)

async def main():
    album_response = await get_response(
        "https://open.spotify.com/album/3539EbNgIdEDGBKkUf4wno"
    )
    album = await get_album_results(album_response)
    caption = await get_caption(album)
    print(caption)


asyncio.run(main())
