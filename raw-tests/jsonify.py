import json
from spotdl import Spotdl
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

spotdl = Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    downloader_settings={"output": "content"},
)


def song_to_dict(song):
    song_dict = {
        "name": song.name,
        "artists": song.artists,
        "artist": song.artist,
        "genres": song.genres,
        "disc_number": song.disc_number,
        "disc_count": song.disc_count,
        "duration": song.duration,
        "year": song.year,
        "date": song.date,
        "track_number": song.track_number,
        "tracks_count": song.tracks_count,
        "song_id": song.song_id,
        "explicit": song.explicit,
        "url": song.url,
        "cover_url": song.cover_url,
        "album_id": song.album_id,
        "file_id": None,
    }

    album_dict = {
        "album_name": song.album_name,
        "album_artist": song.album_artist,
        "album_id": song.album_id,
        "songs": [],
    }

    return song_dict, album_dict


album_id = "5mLmU1wyeAM453ysZZozm2"
album_url = f"https://open.spotify.com/album/{album_id}"

songs = spotdl.search([album_url])


songs_dict = []
albums_dict = []
for song in songs:
    song_dict, album_dict = song_to_dict(song)
    songs_dict.append(song_dict)

    # Check if the album is already in the list
    found = False
    for existing_album_dict in albums_dict:
        if existing_album_dict["album_id"] == album_dict["album_id"]:
            # If the album is already in the list, add the song id to it
            existing_album_dict["songs"].append(song.song_id)
            found = True
            break

    # If the album is not in the list, add it
    if not found:
        album_dict["songs"].append(song.song_id)
        albums_dict.append(album_dict)

with open("songs.json", "w") as f:
    json.dump(songs_dict, f, indent=4)

with open("albums.json", "w") as f:
    json.dump(albums_dict, f, indent=4)
