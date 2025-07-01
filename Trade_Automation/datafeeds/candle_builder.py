import asyncio
from datetime import datetime, timedelta
from logzero import logger
from .types import Candle
from .websocket import tick_buffer
from strategies.ema_spread import Ema9ReversalStrategy
from services.order_executions import handle_strategy_signals


_candles: list[Candle] = []
strategy = Ema9ReversalStrategy()

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
            signals = strategy.on_candle(candle)
            if signals:
                await handle_strategy_signals(strategy.id, signals)
        # sleep until next minute boundary + 1 s safety
        seconds_to_next_boundary = (
            (5 - (now.minute % 5)) * 60 - now.second
        )
        await asyncio.sleep(seconds_to_next_boundary + 1)

def get_all() -> list[Candle]:
    return _candles

from dataclasses import asdict

def get_all_dicts():
    return [
        {
            **asdict(c),
            "time": c.time.isoformat()
        }
        for c in _candles
    ]