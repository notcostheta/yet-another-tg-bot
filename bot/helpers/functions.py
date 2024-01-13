from pyrogram.enums import ChatType, ChatMemberStatus
from pyrogram.types import Message

from bot.configs.config import SUDO_ID


async def isAdmin(message: Message) -> bool:
    """
    Return True if the message is from owner or admin of the group or sudo of the bot.
    """

    if not message.from_user:
        return
    if message.chat.type not in [ChatType.SUPERGROUP, ChatType.CHANNEL]:
        return

    user_id = message.from_user.id
    if user_id in SUDO_ID:
        return True

    check_status = await message.chat.get_member(user_id)
    return check_status.status in [
        ChatMemberStatus.OWNER,
        ChatMemberStatus.ADMINISTRATOR,
    ]
