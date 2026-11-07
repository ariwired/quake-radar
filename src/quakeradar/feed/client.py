from typing import Protocol

from quakeradar.domain.quake import Quake


class FeedClient(Protocol):
    async def fetch(self, feed: str) -> list[Quake]: ...


class NullFeedClient:
    async def fetch(self, feed: str) -> list[Quake]:
        return []
