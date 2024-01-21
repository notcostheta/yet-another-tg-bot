from spotdl import Spotdl
from bot.configs.config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

spotdl =  Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    downloader_settings={"output": "content"},
)
