from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials
from rich import print

spotify = Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id=SPOTIFY_CLIENT_ID, client_secret=SPOTIFY_CLIENT_SECRET
    )
)

# Get the artist's name
artist = "Eminem"

# Search for the artist
response = spotify.search(q=artist, type="artist")

# Get artist id
artist_id = response["artists"]["items"][0]["id"]
print(artist_id)

# Get artist's albums
albums = spotify.artist_albums(artist_id=artist_id, album_type="album")

# Print the artist's albums
print(albums)
