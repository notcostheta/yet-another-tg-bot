# Config Setup for the bot
import json
from dotenv import load_dotenv
from os import getenv

load_dotenv("config.env")

# Get these from my.telegram.org
API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

# Get these from some telgram group manager bots
OWNER_ID = json.loads(getenv("OWNER_ID"))
SUDO_ID = json.loads(getenv("SUDO_ID", "[]"))
SUDO_ID.append(OWNER_ID)

# Session name for the bot
SESSION_NAME = getenv("SESSION_NAME")

# Output Path for storing downloaded files
OUTPUT_PATH = getenv("OUTPUT_PATH")

# Spotify API Keys
SPOTIFY_CLIENT_ID = getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = getenv("SPOTIFY_CLIENT_SECRET")