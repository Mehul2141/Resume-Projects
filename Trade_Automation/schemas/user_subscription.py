from pydantic import BaseModel

class SubscriptionRequest(BaseModel):
    name: str
    email: str
    plan_id: str