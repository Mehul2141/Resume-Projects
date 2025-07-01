# schemas/user_broker.py

from pydantic import BaseModel
from uuid import UUID

class AngelOneLoginRequest(BaseModel):
    broker_id: UUID
    client_code: str
    password: str
    api_key: str
    totp_secret: str

