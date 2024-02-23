from typing import Dict
from bot.helpers.spot import spotdl
from spotdl.types.song import SongList
from spotdl.types.album import Album


async def get_response(query: str) -> SongList:
    try:
        response = spotdl.search([query])
        return response
    except Exception as e:
        return [(e)]


async def get_album_results(response: SongList) -> tuple:
    try:
        id_ = response[0].album_id
        album_url = f"https://open.spotify.com/album/{id_}"
        metadata, album = Album.get_metadata(album_url)
        album = sorted(album, key=lambda song: song.track_number)
        return (metadata, album)
    except Exception as e:
        return [(e)]


async def get_cover_url(response: SongList) -> str:
    try:
        cover_url = response[0].cover_url
        return cover_url
    except Exception as e:
        return [(e)]


async def get_caption(metadata: dict, album: SongList) -> str:
    try:
        artist_id = metadata["artist"]["id"]
        artist_url = f"https://open.spotify.com/artist/{artist_id}"
        album_url = f"https://open.spotify.com/album/{album[0].album_id}"

        caption_header = f"""**Album**: [{album[0].album_name}]({album_url})
**Artists**: [{album[0].album_artist}]({artist_url})
**Release Date**: {album[0].date}
**Total Tracks**: {album[0].tracks_count}
"""
        tracks_str = "\n".join([f"[{track.name}]({track.url})" for track in album])
        caption = f"{caption_header}\n**Tracks**:\n{tracks_str}"
        return caption
    except Exception as e:
        return str(e)
