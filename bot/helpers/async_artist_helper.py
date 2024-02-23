from spotipy.exceptions import SpotifyException
from typing import Dict
from bot.helpers.spot import spotify


async def get_artist_response(artist_name: str) -> dict:
    """
    Retrieves the response for a given artist name from Spotify API.

    Args:
        artist_name (str): The name of the artist.

    Returns:
        dict: The artist response from Spotify API.

    Raises:
        Exception: If an error occurs during the API request.
    """
    try:
        artist_response = spotify.search(q="artist:" + artist_name, type="artist")
        artist_response = artist_response["artists"]["items"][0]
        return artist_response
    except Exception as e:
        return {}


async def get_artist_album_response(artist_response: dict) -> dict:
    """
    Retrieves the album results for a given artist.

    Args:
        artist_response (dict): The artist response dictionary.

    Returns:
        list: The album results list of dictionary.
    """
    try:
        artist_id = artist_response["id"]
        all_albums = []
        album_types = ["album", "single", "compilation"]

        for album_type in album_types:
            albums = spotify.artist_albums(artist_id, album_type=album_type, limit=50)
            all_albums.extend(albums["items"])

            while albums["next"]:
                albums = spotify.next(albums)
                all_albums.extend(albums["items"])

        for album in all_albums:
            album.pop("available_markets", None)

        return all_albums

    except Exception as e:
        return {}


async def get_artist_album_caption(artist_response: dict, album_results: dict) -> str:
    """
    Generate a caption for an artist's albums.

    Args:
        artist_response (dict): The response containing artist information.
        album_results (dict): The response containing album information.

    Returns:
        str: The generated caption for the artist's albums.
    """
    try:
        albums = album_results
        albums.sort(key=lambda x: x["release_date"], reverse=True)
        formatted_albums = [
            f"[{album['name']}]({album['external_urls']['spotify']})"
            for album in albums
        ]
        artist = artist_response["name"]
        caption_header = f"""**Artist**: [{artist}](https://open.spotify.com/artist/{artist_response["id"]})
**Genres**: {", ".join(artist_response['genres'])}
**Followers**: {artist_response['followers']['total']}
**Total Albums**: {len(albums)}
**Recent Albums**:
"""
        # albums_string = "\n".join(formatted_albums)
        # get the first 10 albums
        albums_string = "\n".join(formatted_albums[:10])
        caption = caption_header + albums_string
        return caption
    except Exception as e:
        return "No Artist Found, please try again or try sending a Spotify URL."


async def get_artist_cover(artist_response: dict) -> str:
    """
    Retrieves the cover image URL for a given artist from the artist response.

    Args:
        artist_response (dict): The response containing artist information.

    Returns:
        str: The URL of the artist's cover image.
    """
    try:
        artist_cover = artist_response["images"][0]["url"]
        return artist_cover
    except Exception as e:
        return ""


async def get_album_list(album_results: dict) -> list:
    """
    Retrieves a list of album URLs from the given album results.

    Args:
        album_results (dict): A dictionary containing album results.

    Returns:
        list: A list of album URLs.
    """
    try:

        albums = album_results
        albums.sort(key=lambda x: x["release_date"], reverse=True)
        albums = [album["external_urls"]["spotify"] for album in albums]
        return albums
    except Exception as e:
        return []


async def validate_url(url: str) -> bool:
    """
    Validates a Spotify URL by checking if the artist ID can be retrieved from it.

    Args:
        url (str): The Spotify URL to validate.

    Returns:
        bool: True if the artist ID can be retrieved, False otherwise.
    """
    try:
        artist_id = url.split("/")[-1].split("?")[0]
        artist_response = spotify.artist(artist_id)
        return True
    except Exception as e:
        return False


async def get_artist_response_url(url: str) -> Dict:
    """
    Retrieves the artist response from Spotify API based on the given URL.

    Args:
        url (str): The URL of the artist on Spotify.

    Returns:
        Dict: The artist response from Spotify API.

    Raises:
        SpotifyException: If there is an error while retrieving the artist response.
    """
    try:
        artist_response = spotify.artist(url.split("/")[-1].split("?")[0])
        return artist_response
    except SpotifyException as e:
        return str(e)


# async def main():
#     url = "https://open.spotify.com/artist/7JWTyY1F2DGO4WphbQo2yM"
#     artist = "Far Caspain"
#     # print error message if url is invalid
#     if await validate_url(url) is False:
#         print("Invalid URL")
#     else:
#         artist_response = await get_artist_response_url(url)
#         album_results = await get_artist_album_response(artist_response)
#         caption = await get_artist_album_caption(artist_response, album_results)
#         cover = await get_artist_cover(artist_response)
#         albums = await get_album_list(album_results)
#         print(caption)
#         print(cover)
#         print(albums)


# asyncio.run(main())
