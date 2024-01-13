from typing import Union

from pyrate_limiter import (
    BucketFullException,
    Duration,
    Limiter,
    Rate,
)


class RateLimiter:
    """
    Implement rate limit logic using leaky bucket
    algorithm, via pyrate_limiter.
    (https://pypi.org/project/pyrate-limiter/)
    """

    def __init__(self) -> None:
        # 2 requests per seconds
        self.second_rate = Rate(2, Duration.SECOND)

        # 17 requests per minute.
        self.minute_rate = Rate(17, Duration.MINUTE)

        # 1000 requests per hour
        self.hourly_rate = Rate(1000, Duration.HOUR)

        # 10000 requests per day
        self.daily_rate = Rate(10000, Duration.DAY)

        rates = [self.second_rate, self.minute_rate, self.hourly_rate, self.daily_rate]
        self.limiter = Limiter(rates)

    async def acquire(self, userid: Union[int, str]) -> bool:
        """
        Acquire rate limit per userid and return True / False
        based on userid ratelimit status.
        """

        try:
            self.limiter.try_acquire(userid)
            return False
        except BucketFullException:
            return True
