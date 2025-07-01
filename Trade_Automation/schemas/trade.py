# schemas/trade.py
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class TradeResponse(BaseModel):
    trade_id: UUID
    symbol: str
    trade_datetime: datetime
    order_type: str
    quantity: int
    entry_price: float
    exit_price: float
    profit_loss: float
    status: str
    created_at: datetime
