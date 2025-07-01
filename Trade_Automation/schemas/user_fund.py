from pydantic import BaseModel
from datetime import datetime

class FundSchema(BaseModel):
    margin_used : float
    funds_available : float
    last_updated : datetime
