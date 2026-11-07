from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class MongoSettings(BaseModel):
    connection_string: str = "mongodb://localhost:27017/?directConnection=true"
    database: str = "quakeradar"
    retention_days: int = 30


class CollectorSettings(BaseModel):
    base_url: str = "https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/"
    backfill_feed: str = "all_month"
    live_feed: str = "all_hour"
    interval_seconds: int = 60


class AlertSettings(BaseModel):
    min_magnitude: float = 5.0
    max_event_age_hours: int = 6
    webhook_url: str = ""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_nested_delimiter="__", env_file=".env", extra="ignore")

    mongo: MongoSettings = MongoSettings()
    collector: CollectorSettings = CollectorSettings()
    alert: AlertSettings = AlertSettings()
