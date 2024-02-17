import json
from spotdl import Spotdl
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET
from spotdl.types.artist import Artist
from spotdl.types.playlist import Playlist
from spotdl.types.album import Album


spotdl = Spotdl(
    client_id=SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET,
    downloader_settings={"output": "content"},
)


def get_response(query):
    try:
        response = spotdl.search([query])
        return response
    except Exception as e:
        return str(e)


def get_album_results(response):
    try:
        id_ = response[0].album_id
        album_url = f"https://open.spotify.com/album/{id_}"
        album = spotdl.search([album_url])
        return album
    except Exception as e:
        return str(e)


def get_tracks(album):
    tracks_dict = {}
    for track in album:
        track_name = track.name
        artists = track.artists
        tracks_dict[track_name] = artists
    return tracks_dict


def generate_caption(query):
    response = get_response(query)
    album = get_album_results(response)
    tracks = get_tracks(album)

    album_name = album[0].album_name
    album_artist = album[0].album_artist
    artists = ", ".join(album[0].artists)
    release_date = album[0].date

    tracks_str = "\n".join([f"{track}" for track, artists in tracks.items()])

    caption = f"""
*Album*: {album_name}
*Artists*: {album_artist}
*Release Date*: {release_date}

*Tracks*:
{tracks_str}
"""

    return caption


# print(generate_caption("the pocket gods"))

artist_test = "https://open.spotify.com/artist/0EzsHuJxUDcfqSqvoPhKG4?si=Wj_VapIHRV6OaJcDxWdhPw"
playlist = "https://open.spotify.com/playlist/15MQ0IeUvXoW4eGyt9bNtY?si=bab7120f39bb44de"
album_test = "https://open.spotify.com/album/7FmLx521t1FJ6bWggcuNCY"

# print(get_response(playlist))
# print(get_response(artist_test))

def get_artist(url):
    try:
        response = Artist.get_metadata(url)
        metadata = response[0]
        songlist = response[1]
        return metadata, songlist
    except Exception as e:
        return str(e)
    
# print(get_artist(artist_test))

def get_playlist(url):
    try:
        response = Playlist.get_metadata(url)
        metadata = response[0]
        songlist = response[1]
        
        return metadata, songlist
    except Exception as e:
        return str(e)
    
def get_album(url):
    try:
        response = Album.get_metadata(url)
        metadata = response[0]
        songlist = response[1]
        
        return metadata, songlist
    except Exception as e:
        return str(e)

metadata, songlist = get_album(album_test)
print(metadata)

artist , songlist = get_artist(artist_test)
print(artist)
