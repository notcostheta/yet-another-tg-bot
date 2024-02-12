import json
from spotdl import Spotdl
from config import SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET

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


from rich import print
import textwrap


def generate_caption(query):
    response = get_response(query)
    album = get_album_results(response)
    tracks = get_tracks(album)

    album_name = album[0].album_name
    album_artist = album[0].album_artist
    artists = ", ".join(album[0].artists)
    release_date = album[0].date

    # tracks_str = "\n".join(
    #     [
    #         f"{track}: {textwrap.fill(', '.join(artists), width=36)}"
    #         for track, artists in tracks.items()
    #     ]
    # )

    tracks_str = "\n".join([f"{track}" for track, artists in tracks.items()])

    caption = f"""
*Album*: {album_name}
*Artists*: {album_artist}
*Release Date*: {release_date}

*Tracks*:
{tracks_str}
"""

    return caption


print(generate_caption("the pocket gods"))
