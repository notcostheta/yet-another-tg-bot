import time
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.helpers.decorators import ratelimiter
from bot.configs.config import CACHE_CHANNEL
from bot.helpers.filters import dev_cmd
from bot.helpers.spot import spotdl
from tqdm import tqdm
import asyncio
from concurrent.futures import ProcessPoolExecutor
from bot.utils.logging import LOGGER

logger = LOGGER(__name__)

@Client.on_message(filters.command("max", prefixes="."))
@ratelimiter
async def max_length(_, message: Message):
    await message.reply_text("0" * 4096)
    print(len("0000000000000000000000000000000000000000000000000000000"))
    print(len("000000000000000000000000000000000000000"))