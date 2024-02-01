"""
Creating custom filters 
https://docs.pyrogram.org/topics/create-filters
"""

from pyrogram import filters
from pyrogram.types import Message
from bot.configs.config import SUDO_ID, OWNER_ID


def dev_users(_, __, message: Message) -> bool:
    return message.from_user.id in OWNER_ID if message.from_user else False


def sudo_users(_, __, message: Message) -> bool:
    return message.from_user.id in SUDO_ID if message.from_user else False


def valid_users(_, __, message: Message) -> bool:
    user = message.from_user
    if user.is_bot or user.is_deleted or user.is_scam or user.is_fake:
        return False
    else:
        return True


dev_cmd = filters.create(dev_users)
sudo_cmd = filters.create(sudo_users)
user_cmd = filters.create(valid_users)
