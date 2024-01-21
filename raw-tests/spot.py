from spotdl import Spotdl
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

spotdl = Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    downloader_settings={"output": "content"},
)

# text = str(input("Enter the song name: "))
text = "Vansire"
text2 = "Vansire - Nice To See You (feat. Floor Cry)"

search = spotdl.search([text, text2])
song, path = spotdl.download(search[0])

# print(search)
print(song)
# print(path)
