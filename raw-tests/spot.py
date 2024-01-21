from spotdl import Spotdl
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

spotdl = Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    downloader_settings={"output": "content"},
)


def download_song(url):
    try:
        search = spotdl.search([url])
        song, path = spotdl.download(search[0])
        return song, path
    except Exception as e:
        return str(e)


song_name = "Vansire"
song_obj = download_song(song_name)[0]

print(song_obj)