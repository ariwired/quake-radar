import asyncio
from collections.abc import AsyncIterator, Sequence
from datetime import UTC, datetime

from quakeradar.config import CollectorSettings
from quakeradar.domain.quake import Quake
from quakeradar.workers.collector import UsgsCollector
from quakeradar.workers.watcher import AlertWatcher


def make_quake(id: str = "us1") -> Quake:
    return Quake(id, 5.1, "45 km SE of Hitachi, Japan", datetime.now(UTC), 38.2, None, 140.9, 36.3)


class FakeFeed:
    def __init__(self, quakes: list[Quake]) -> None:
        self.quakes = quakes
        self.calls: list[str] = []

    async def fetch(self, feed: str) -> list[Quake]:
        self.calls.append(feed)
        return self.quakes


class FakeRepo:
    def __init__(self, to_watch: list[Quake] | None = None) -> None:
        self.upserted: list[Quake] = []
        self.to_watch = to_watch or []

    async def upsert_many(self, quakes: Sequence[Quake]) -> None:
        self.upserted.extend(quakes)

    async def watch_inserts(self) -> AsyncIterator[Quake]:
        for quake in self.to_watch:
            yield quake
        await asyncio.Event().wait()


class FakeDispatcher:
    def __init__(self) -> None:
        self.seen: list[Quake] = []

    async def dispatch(self, quake: Quake) -> None:
        self.seen.append(quake)


async def test_collector_runs_backfill_then_live_feed():
    feed = FakeFeed([make_quake()])
    repo = FakeRepo()
    settings = CollectorSettings(interval_seconds=0)
    task = asyncio.create_task(UsgsCollector(feed, repo, settings).run())
    await asyncio.sleep(0.05)
    task.cancel()
    assert feed.calls[0] == "all_month"
    assert "all_hour" in feed.calls
    assert repo.upserted


async def test_watcher_dispatches_each_inserted_quake():
    quakes = [make_quake("a"), make_quake("b")]
    dispatcher = FakeDispatcher()
    task = asyncio.create_task(AlertWatcher(FakeRepo(quakes), dispatcher).run())
    await asyncio.sleep(0.05)
    task.cancel()
    assert [q.id for q in dispatcher.seen] == ["a", "b"]
