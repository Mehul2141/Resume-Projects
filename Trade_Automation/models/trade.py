from sqlalchemy import (
    Column, String, Integer, ForeignKey, DateTime, Text, DECIMAL, UniqueConstraint
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship, declarative_base
from core.database import Base
import datetime
import uuid

class Trade(Base):
    __tablename__ = 'trades'

    trade_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.user_id'))
    symbol = Column(String)
    trade_datetime = Column(DateTime(timezone=True))
    order_type = Column(String)
    quantity = Column(Integer)
    entry_price = Column(DECIMAL)
    exit_price = Column(DECIMAL)
    profit_loss = Column(DECIMAL)
    status = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", back_populates="trades")