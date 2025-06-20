from dataclasses import dataclass
from datetime import datetime

@dataclass(slots=True, frozen=True)
class Tick:
    timestamp: datetime
    price: float

@dataclass(slots=True, frozen=True)
class Candle:
    time: datetime
    open: float
    high: float
    low: float
    close: float