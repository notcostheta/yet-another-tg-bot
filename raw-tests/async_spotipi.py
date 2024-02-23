import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
import sys
import asyncio
from rich import print
from typing import Dict

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
)


async def get_response(name: str) -> dict:
    try:
        results = spotify.search(q="artist:" + name, type="artist")
        return results
    except Exception as e:
        return str(e)


async def get_artist_caption(results: dict) -> str:
    artist = results["artists"]["items"][0]
    artist_id = artist["id"]

    results = spotify.artist_albums(artist_id, album_type="album")
    albums = results["items"]
    albums.sort(key=lambda x: x["release_date"], reverse=True)
    formatted_albums = [
        f"[{album['name']}]({album['external_urls']['spotify']})" for album in albums
    ]
    caption_header = f"""**Artist**: [{artist['name']}](https://open.spotify.com/artist/{artist['id']})
**Genres**: {", ".join(artist['genres'])}
**Followers**: {artist['followers']['total']}
**Albums**:
"""
    albums_string = "\n".join(formatted_albums)
    caption = caption_header + albums_string
    return caption


async def get_artist_cover(results: dict) -> str:
    artist = results["artists"]["items"][0]
    return artist["images"][0]["url"]


async def get_album_list(results: dict) -> list:
    artist = results["artists"]["items"][0]
    artist_id = artist["id"]
    results = spotify.artist_albums(artist_id, album_type="album")
    albums = results["items"]
    albums.sort(key=lambda x: x["release_date"], reverse=True)
    # albums = [album["external_urls"]["spotify"] for album in albums]
    albums = [album["id"] for album in albums]
    return albums


async def main():
    results = await get_response("The Rolling Stones")
    caption = await get_artist_caption(results)
    cover = await get_artist_cover(results)
    albums = await get_album_list(results)
    print(len(albums))
    # print(cover)
    # print(caption)
    # print(results)


asyncio.run(main())
