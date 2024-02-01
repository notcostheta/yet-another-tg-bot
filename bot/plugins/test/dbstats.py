from pyrogram.types import Message
from pyrogram import Client, filters

from bot.database.MongoDb import users, chats
from bot.helpers.decorators import ratelimiter
from bot.helpers.filters import sudo_cmd


@Client.on_message(filters.command("db"))
@ratelimiter
async def dbstats(client: Client, message: Message):
    total_users = await users.total_documents()
    total_chats = await chats.total_documents()
    await message.reply_text(
        f"Total Users in DB: {total_users}\nTotal Chats in DB: {total_chats}"
    )
