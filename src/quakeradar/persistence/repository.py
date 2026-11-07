import asyncio
from collections.abc import AsyncIterator, Sequence
from typing import Protocol

from quakeradar.domain.quake import Quake


class QuakeRepository(Protocol):
    async def upsert_many(self, quakes: Sequence[Quake]) -> None: ...

    def watch_inserts(self) -> AsyncIterator[Quake]: ...


class NullQuakeRepository:
    async def upsert_many(self, quakes: Sequence[Quake]) -> None:
        return None

    async def watch_inserts(self) -> AsyncIterator[Quake]:
        await asyncio.Event().wait()
        for quake in ():
            yield quake
