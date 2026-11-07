from typing import Protocol

from quakeradar.domain.quake import Quake


class AlertDispatcher(Protocol):
    async def dispatch(self, quake: Quake) -> None: ...


class NullAlertDispatcher:
    async def dispatch(self, quake: Quake) -> None:
        return None
