from dataclasses import dataclass
from typing import List, Literal

from core.indicators import EMA
from datafeeds.types import Candle

# ──────────────────────────────────────────────────────────────
@dataclass(slots=True)
class Signal:
    side: Literal["SELL"]        # this strategy only shorts
    price: float                 # entry @ candle.close
    sl: float                    # stop‑loss
    tp: float                    # take‑profit
    qty: int                     # to be filled by executor
    candle_time: str             # ISO timestamp for audit
# ──────────────────────────────────────────────────────────────


class Ema9ReversalStrategy:
    """
    Short when price stretches above EMA‑9 and shows a bearish rejection candle.
    """

    id = "ema9_reversal"         # must match DB strategy_id

    def __init__(
        self,
        threshold_pct: float = 0.3,   # price must be ≥ 0.3 % above EMA‑9
        wick_pct: float = 0.5,        # top wick ≥ 0.5 % of close
        rr: float = 2.0              # risk‑reward (TP distance = rr × risk)
    ):
        self.ema = EMA(9)
        self.threshold_pct = threshold_pct
        self.wick_pct = wick_pct
        self.rr = rr
        self.candle_count = 0

    # ----------------------------------------------------------
    def on_candle(self, candle: Candle) -> List[Signal]:
        self.candle_count += 1
        ema_val = self.ema.update(candle.close)

        if self.candle_count < self.ema.period:
            return [] 

        if ema_val is None:          # need at least 9 data points
            return []

        # 1️⃣ Stretch above EMA
        diff_pct = (candle.close - ema_val) / ema_val * 100
        if diff_pct < self.threshold_pct:
            return []

        # 2️⃣ Bearish candle (red)
        if candle.close >= candle.open:
            return []

        # 3️⃣ Long upper wick
        top_wick = candle.high - candle.close
        if top_wick < self.wick_pct / 100 * candle.close:
            return []

        # ---- All conditions met → build signal ----------------
        sl = candle.high * 1.0001          # small buffer (0.01 %)
        risk = sl - candle.close
        tp = candle.close - self.rr * risk

        signal = Signal(
            side="SELL",
            price=candle.close,
            sl=sl,
            tp=tp,
            qty=0,                         # executor will fill per‑user
            candle_time=candle.time.isoformat(timespec="seconds"),
        )
        return [signal]
