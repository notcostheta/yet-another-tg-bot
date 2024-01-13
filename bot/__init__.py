import sys
import time
from asyncio import get_event_loop, new_event_loop, set_event_loop
import uvloop

from pyrogram import Client
from bot.configs import config
from bot.utils.logging import LOGGER

uvloop.install()
LOGGER(__name__).info("Starting the bot....")
BotStartTime = time.time()

# Check if the python version is 3.10 or above
if sys.version_info[0] != 3 or sys.version_info[1] < 10:
    LOGGER(__name__).fatal(
        "You MUST have a python version of at least 3.10! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

# Set up the event loop
LOGGER(__name__).info("Setting up event loop....")
try:
    loop = get_event_loop()
except RuntimeError:
    set_event_loop(new_event_loop())
    loop = get_event_loop()

# Set up the bot client
LOGGER(__name__).info("Setting up bot client....")
app = Client(
    config.SESSION_NAME,
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    plugins=dict(root="bot/plugins"),
)