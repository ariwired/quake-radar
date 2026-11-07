import asyncio
import logging

from quakeradar.config import CollectorSettings
from quakeradar.feed.client import FeedClient
from quakeradar.persistence.repository import QuakeRepository

log = logging.getLogger(__name__)


class UsgsCollector:
    def __init__(self, feed: FeedClient, repo: QuakeRepository, settings: CollectorSettings) -> None:
        self._feed = feed
        self._repo = repo
        self._settings = settings

    async def run(self) -> None:
        await self._collect(self._settings.backfill_feed)
        while True:
            await asyncio.sleep(self._settings.interval_seconds)
            await self._collect(self._settings.live_feed)

    async def _collect(self, feed_name: str) -> None:
        try:
            quakes = await self._feed.fetch(feed_name)
            if not quakes:
                return
            await self._repo.upsert_many(quakes)
            log.info("Feed %s: %d eventos gravados", feed_name, len(quakes))
        except asyncio.CancelledError:
            raise
        except Exception:
            log.exception("Falha ao coletar o feed %s", feed_name)
