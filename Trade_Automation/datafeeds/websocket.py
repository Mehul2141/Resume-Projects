from SmartApi.smartWebSocketV2 import SmartWebSocketV2
from logzero import logger
from datetime import datetime, timedelta
from collections import defaultdict
from core.config import settings
from services.brokers.angelone import get_auth_tokens
from .types import Tick

EXCHANGE_TOKEN = "26009"   # NIFTY
EXCHANGE_TYPE  = 1
MODE           = 1
CORRELATION_ID = "abc123"

_all_ = ["sws", "tick_buffer"]

# shared dict; candle_builder consumes it
tick_buffer: defaultdict[datetime, list[Tick]] = defaultdict(list)

def _build_sws() -> SmartWebSocketV2:
    jwt, feed, _ = get_auth_tokens(
        client_code=settings.ANGELONE_CLIENTCODE,
        password=settings.ANGELONE_APP_PASSWORD,
        totp_key=settings.ANGELONE_TOTP_SECRET,
    )

    sws = SmartWebSocketV2(
        auth_token=jwt,
        api_key=settings.ANGELONE_API_KEY,
        client_code=settings.ANGELONE_CLIENTCODE,
        feed_token=feed,
    )

    # -----------------------------------------------------------------
    def on_data(wsapp, msg):
        try:
            ltp = msg["last_traded_price"] / 100
            ts  = datetime.fromtimestamp(msg["exchange_timestamp"] / 1000)
            bucket = ts.replace(second=0, microsecond=0) - timedelta(minutes=ts.minute % 5)
            tick_buffer[bucket].append(Tick(ts, ltp))
        except Exception as exc:
            logger.error(f"tick parse error {exc}")

    def on_open(wsapp):
        logger.info("WebSocket opened")
        sws.subscribe(CORRELATION_ID, MODE, [{
            "exchangeType": EXCHANGE_TYPE,
            "tokens": [EXCHANGE_TOKEN],
        }])

    sws.on_open  = on_open
    sws.on_data  = on_data
    sws.on_error = lambda *_: logger.exception("WebSocket error")
    sws.on_close = lambda *_: logger.warning("WebSocket closed")

    return sws
# ---------------------------------------------------------------------

sws = _build_sws()    # ← importable singleton