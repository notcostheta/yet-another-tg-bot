from functools import wraps
from typing import Callable, Union
from pyrogram import Client
from pyrogram.types import CallbackQuery, Message
from cachetools import TTLCache

from bot.helpers.functions import isAdmin
from bot.helpers.ratelimiter import RateLimiter

ratelimit = RateLimiter()
warned_users = TTLCache(maxsize=128, ttl=60)
warning_message = "You are being rate limited. Please try again after 60 seconds."


def ratelimiter(func: Callable) -> Callable:
    """
    Restricts users from spamming commands or pressing buttons multiple times
    using the leaky bucket algorithm and pyrate_limiter.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.

    Raises:
        BucketFullException: If the user has exceeded the rate limit.

    Example:
        @ratelimiter
        async def my_command(client, update):
            # Function implementation
    """

    @wraps(func)
    async def decorator(client: Client, update: Union[Message, CallbackQuery]):
        userid = update.from_user.id
        is_limited = await ratelimit.acquire(userid)

        if is_limited and userid not in warned_users:
            if isinstance(update, Message):
                await update.reply_text(warning_message)
                warned_users[userid] = 1
                return

            elif isinstance(update, CallbackQuery):
                await update.answer(warning_message, show_alert=True)
                warned_users[userid] = 1
                return

        elif is_limited and userid in warned_users:
            pass
        else:
            return await func(client, update)

    return decorator


def admin_commands(func: Callable) -> Callable:
    """
    Restricts users from using group admin commands.

    This decorator can be used to restrict the usage of certain commands to group admins only.
    It checks if the user sending the message is an admin, and if not, the command is not executed.

    Args:
        func (Callable): The function to be decorated.

    Returns:
        Callable: The decorated function.
    """

    @wraps(func)
    async def decorator(client: Client, message: Message):
        if await isAdmin(message):
            return await func(client, message)

    return decorator
