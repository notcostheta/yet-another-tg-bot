# Config Setup for the bot
from dotenv import load_dotenv
from os import getenv

load_dotenv("config.env")

# Spotify API Credentials
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")
