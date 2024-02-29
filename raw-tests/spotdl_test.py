import asyncio
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from spotdl import Spotdl
from spotdl.types.song import SongList
from spotdl.types.album import Album
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


async def get_album_results(response: SongList) -> tuple:
    try:
        id_ = response[0].album_id
        album_url = f"https://open.spotify.com/album/{id_}"
        metadata, album = Album.get_metadata(album_url)
        album = sorted(album, key=lambda song: song.track_number)
        return (metadata, album)
    except Exception as e:
        return [(e)]


async def main():
    song_url = "vallis alps"
    response = await get_response(song_url)
    metadata, album = await get_album_results(response)
    # print(metadata)
    print(album)

    # print the most popular songs in the album
    print("Most popular songs in the album:")
    for song in album[:5]:
        print(f"{song.name} - {song.popularity}% popularity")
        

asyncio.run(main())
