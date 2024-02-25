from typing import Dict, Tuple
from bot.helpers.spot import spotdl
from spotdl.types.playlist import SongList
from spotdl.types.playlist import Playlist


async def get_response(query: str) -> tuple:
    """
    Retrieves the metadata and playlist for a given query.

    Args:
        query (str): The query to search for.

    Returns:
        tuple: A tuple containing the metadata and playlist.
        Metadata is a dictionary containing the metadata of the playlist.
        Playlist is a list of SongObjects in the playlist.

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
