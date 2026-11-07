from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class Quake:
    id: str
    mag: float | None
    place: str
    time: datetime
    depth_km: float | None
    url: str | None
    lon: float
    lat: float
