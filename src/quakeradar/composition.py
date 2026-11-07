from dataclasses import dataclass

from quakeradar.alerts.dispatcher import AlertDispatcher, NullAlertDispatcher
from quakeradar.config import Settings
from quakeradar.feed.client import FeedClient, NullFeedClient
from quakeradar.persistence.repository import NullQuakeRepository, QuakeRepository
from quakeradar.workers.collector import UsgsCollector
from quakeradar.workers.watcher import AlertWatcher


@dataclass(frozen=True, slots=True)
class Container:
    settings: Settings
    feed: FeedClient
    repo: QuakeRepository
    dispatcher: AlertDispatcher
    collector: UsgsCollector
    watcher: AlertWatcher


def build_container(settings: Settings | None = None) -> Container:
    settings = settings or Settings()
    feed = NullFeedClient()
    repo = NullQuakeRepository()
    dispatcher = NullAlertDispatcher()
    return Container(
        settings=settings,
        feed=feed,
        repo=repo,
        dispatcher=dispatcher,
        collector=UsgsCollector(feed, repo, settings.collector),
        watcher=AlertWatcher(repo, dispatcher),
    )
