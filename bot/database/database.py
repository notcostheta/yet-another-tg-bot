from bot.database import MongoDb as db
from datetime import datetime, timezone
from bot.utils.logging import LOGGER
import pyrogram

logger = LOGGER(__name__)


async def save_user(user):
    """
    Saves user to database
    Args: user (pyrogram.types.User): User to save
    Returns: None
    """
    try:
        insert_format = {
            "name": (user.first_name or " ") + (user.last_name or ""),
            "username": user.username,
            "date": datetime.now(timezone.utc),
            "perma_link": user.mention,
            "photo": user.photo.big_file_id if user.photo else None,
        }
        await db.users.update_document(user.id, insert_format)
        logger.info(f"User {user.id} saved")
    except Exception as e:
        logger.error(f"Error saving {user.id}: {e}")


async def save_chat(chat_id):
    try:
        insert_format = {"date": datetime.now(timezone.utc)}
        await db.chats.update_document(chat_id, insert_format)
        logger.info(f"Chat {chat_id} saved")
    except Exception as e:
        logger.error(f"Error saving {chat_id}: {e}")


async def save_track(song):
    try:
        insert_format = {
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
            "users": [],
        }
        await db.tracks.update_document(song.song_id, insert_format)
    except Exception as e:
        logger.error(f"Error saving track: {e}")


async def save_album(song):
    try:
        insert_format = {
            "album_name": song.album_name,
            "album_artist": song.album_artist,
            "album_id": song.album_id,
            "cover_file_id": None,
            "songs": [],
            "users": [],
        }
        await db.albums.update_document(song.album_id, insert_format)
    except Exception as e:
        logger.error(f"Error saving album: {e}")


async def update_file_id(song_id, file_id):
    try:
        update_format = {"file_id": file_id}
        await db.tracks.update_document(song_id, update_format)
    except Exception as e:
        logger.error(f"Error updating file_id for song {song_id}: {e}")


async def update_user_song(song_id, user_id):
    try:
        update_format = {"$push": {"users": user_id}}
        await db.tracks.update_document(song_id, update_format)
    except Exception as e:
        logger.error(f"Error updating user for song {song_id}: {e}")


async def update_user_album(album_id, user_id):
    try:
        update_format = {"$push": {"users": user_id}}
        await db.albums.update_document(album_id, update_format)
    except Exception as e:
        logger.error(f"Error updating user for album {album_id}: {e}")


async def update_album_cover(album_id, file_id):
    try:
        update_format = {"cover_file_id": file_id}
        await db.albums.update_document(album_id, update_format)
    except Exception as e:
        logger.error(f"Error updating cover for album {album_id}: {e}")


async def update_album_song(album_id, song_id):
    try:
        update_format = {"$push": {"songs": song_id}}
        await db.albums.update_document(album_id, update_format)
    except Exception as e:
        logger.error(f"Error updating song for album {album_id}: {e}")
