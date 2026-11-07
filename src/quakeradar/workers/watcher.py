import asyncio
import logging

from quakeradar.alerts.dispatcher import AlertDispatcher
from quakeradar.persistence.repository import QuakeRepository

log = logging.getLogger(__name__)

RETRY_DELAY_SECONDS = 5


class AlertWatcher:
    def __init__(self, repo: QuakeRepository, dispatcher: AlertDispatcher) -> None:
        self._repo = repo
        self._dispatcher = dispatcher

    async def run(self) -> None:
        while True:
            try:
                async for quake in self._repo.watch_inserts():
                    try:
                        await self._dispatcher.dispatch(quake)
                    except Exception:
                        log.exception("Falha ao despachar alerta de %s", quake.id)
            except asyncio.CancelledError:
                raise
            except Exception:
                log.warning("Change stream interrompido, reabrindo em %ds", RETRY_DELAY_SECONDS, exc_info=True)
            await asyncio.sleep(RETRY_DELAY_SECONDS)
