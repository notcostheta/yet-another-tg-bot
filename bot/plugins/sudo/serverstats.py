import os
import time
import shutil
import psutil
from datetime import datetime

from pyrogram import Client, filters
from pyrogram.types import Message

from bot import BotStartTime
from bot.helpers.filters import sudo_cmd
from bot.helpers.decorators import ratelimiter
from bot.helpers.functions import get_readable_bytes, get_readable_time


@Client.on_message(filters.command(["stats"]) & sudo_cmd)
@ratelimiter
async def stats(_, message: Message):
    total, used, free = shutil.disk_usage(".")
    process = psutil.Process(os.getpid())

    botuptime = get_readable_time(time.time() - BotStartTime)
    osuptime = get_readable_time(time.time() - psutil.boot_time())
    botusage = f"{round(process.memory_info()[0]/1024 ** 2)} MiB"

    upload = get_readable_bytes(psutil.net_io_counters().bytes_sent)
    download = get_readable_bytes(psutil.net_io_counters().bytes_recv)

    cpu_percentage = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()

    ram_percentage = psutil.virtual_memory().percent
    ram_total = get_readable_bytes(psutil.virtual_memory().total)
    ram_used = get_readable_bytes(psutil.virtual_memory().used)

    disk_percenatge = psutil.disk_usage("/").percent
    disk_total = get_readable_bytes(total)
    disk_used = get_readable_bytes(used)
    disk_free = get_readable_bytes(free)

    caption = f"**OS Uptime:** {osuptime}\n**Memory Usage:** {botusage}\n\n**Total Space:** {disk_total}\n**Free Space:** {disk_free}\n\n**Download:** {download}\n**Upload:** {upload}"

    start = datetime.now()
    msg = await message.reply_text(
        text=caption,
        quote=True,
    )
    end = datetime.now()

    cpu_info = f"CPU Info: {cpu_count} core, {cpu_percentage}%"
    disk_info = f"Disk Info: {disk_used} / {disk_total}, {disk_percenatge}%"
    ram_info = f"RAM Info: {ram_used} / {ram_total}, {ram_percentage}%"
    bot_info = f"Bot Uptime: {botuptime}"
    response_time = f"Response Time: {(end-start).microseconds/1000} ms"

    final_message = (
        f"{caption}\n\n{cpu_info}\n{disk_info}\n{ram_info}\n{bot_info}\n{response_time}"
    )
    await msg.edit_text(text=final_message)
