from pydantic import BaseModel, EmailStr

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class JWTBearer(BaseModel):
    access_token: str

class ResponseSchema(BaseModel):
    trade_id: str
    symbol: str
    trade_datetime: str
    order_type: str
    quantity: int
    entry_price: float
    exit_price: float
    profit_loss: float
    status: str
    created_at: str