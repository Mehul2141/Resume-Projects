import asyncio
from datetime import datetime, timedelta
from logzero import logger
from .types import Candle
from .websocket import tick_buffer

_candles: list[Candle] = []

async def run():
    """Background coroutine that turns ticks → 5-min candles."""
    while True:
        now  = datetime.now()
        past = now.replace(second=0, microsecond=0) - timedelta(minutes=(now.minute % 5 or 5))

        if past in tick_buffer:
            prices = [t.price for t in tick_buffer.pop(past)]
            candle = Candle(
                time=past,
                open=prices[0],
                high=max(prices),
                low=min(prices),
                close=prices[-1],
            )
            _candles.append(candle)
            logger.info(f"Candle {candle}")

        # sleep until next minute boundary + 1 s safety
        await asyncio.sleep(61 - now.second)

def get_all() -> list[Candle]:
    return _candles