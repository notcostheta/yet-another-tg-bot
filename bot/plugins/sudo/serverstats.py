import os
import time
import shutil
import psutil

from pyrogram import filters, Client
from pyrogram.types import Message

from bot import BotStartTime
from bot.helpers.filters import sudo_cmd
from bot.helpers.decorators import ratelimiter


def create_progress_bar(percentage: float, total_length: int) -> str:
    filled_length = int(round(total_length * percentage / 100))  # round the value to get the closest integer
    bar = "█" * filled_length + "-" * (total_length - filled_length)
    return f"{percentage:.2f}% |{bar}|"


@Client.on_message(filters.command("serverstats") & sudo_cmd)
@ratelimiter
async def serverstats(client: Client, message: Message):
    uptime = time.time() - BotStartTime
    uptime_str = time.strftime("%H:%M:%S", time.gmtime(uptime))

    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent

    disk_usage = shutil.disk_usage("/")
    total_disk_space = disk_usage.total
    used_disk_space = disk_usage.used
    disk_usage_percent = (used_disk_space / total_disk_space) * 100

    cpu_usage_bar = create_progress_bar(cpu_usage, 20)
    memory_usage_bar = create_progress_bar(memory_usage, 20)
    disk_usage_bar = create_progress_bar(disk_usage_percent, 20)

    await message.reply_text(
        f"Server Stats:\n"
        f"Uptime: {uptime_str}\n"
        f"CPU Usage: {cpu_usage_bar}\n"
        f"Memory Usage: {memory_usage_bar}\n"
        f"Disk Usage: {disk_usage_bar}"
    )
