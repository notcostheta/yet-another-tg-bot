import asyncio
from spotdl import Spotdl
from spotdl.types.playlist import SongList
from spotdl.types.playlist import Playlist
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from rich import print

spotdl = Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    downloader_settings={"output": "content"},
)


async def get_response(query: str) -> tuple:
    """
    Retrieves the metadata and playlist for a given query.

    Args:
        query (str): The query to search for.

    Returns:
        tuple: A tuple containing the metadata and playlist.

    Raises:
        Exception: If an error occurs during the retrieval process.
    """
    try:
        metadata, playlist = Playlist.get_metadata(query)
        return (metadata, playlist)
    except Exception as e:
        return [(e)]


async def get_cover_url(metadata: dict) -> str:
    """
    Get the cover URL from the metadata dictionary.

    Args:
        metadata (dict): The metadata dictionary containing the cover URL.

    Returns:
        str: The cover URL.

    Raises:
        Exception: If the cover URL is not found in the metadata dictionary.
    """
    try:
        cover_url = metadata["cover_url"]
        return cover_url
    except Exception as e:
        return [(e)]


async def get_caption(metadata: dict, playlist: SongList) -> str:
    """
    Generate the caption for a playlist.

    Args:
        metadata (dict): The metadata of the playlist.
        playlist (SongList): The list of songs in the playlist.

    Returns:
        str: The generated caption for the playlist.
    """
    try:
        caption_header = f"""**Playlist**: [{metadata["name"]}]({metadata["url"]})
**By**: [{metadata["author_name"]}]({metadata["author_url"]})
**Total Tracks**: {len(playlist)}
"""
        return caption_header
    except Exception as e:
        return str(e)


# async def main():
#     query = (
#         "https://open.spotify.com/playlist/15MQ0IeUvXoW4eGyt9bNtY?si=a29acbe0681a4cd9"
#     )
#     metadata, playlist = await get_response(query)
#     cover = await get_cover_url(metadata)
#     caption = await get_caption(metadata, playlist)
#     print(cover)
#     print(caption)


# asyncio.run(main())
