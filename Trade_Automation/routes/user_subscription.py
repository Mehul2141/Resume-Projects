# main.py
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from core.razorpay_client import razorpay_client
import time
from schemas.user_subscription import SubscriptionRequest
router = APIRouter(prefix="/subscribe", tags=["Subscription"])


@router.post("/create-subscription")
def create_subscription(data: SubscriptionRequest):
    try:
        customer = razorpay_client.customer.create({
            "name": data.name,
            "email": data.email
        })

    
        subscription = razorpay_client.subscription.create({
            "plan_id": data.plan_id,
            "customer_notify": 1,
            "total_count": 12,     # 0 = infinite
            # "start_at": int(time.time()) + 60,
            "addons": [{
            "item": {
            "name": "Starter Plan - Test",
            "amount": 499,     # ₹100.00 (in paise)
            "currency": "INR"}}
            ]
        })

        return {
            "subscription_id": subscription["id"],
            "short_url": subscription["short_url"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


from pydantic import BaseModel
class PlanRequest(BaseModel):
    name: str
    amount: int  # In paise (e.g., ₹100 = 10000)
    currency: str = "INR"
    interval: int = 1
    period: str = "monthly"
    description: str = "API-created plan"

@router.post("/create-plan")
def create_plan(plan: PlanRequest):
    try:
        plan_data = {
            "period": plan.period,
            "interval": plan.interval,
            "item": {
                "name": plan.name,
                "amount": plan.amount,
                "currency": plan.currency,
                "description": plan.description,
            },
            "charge_at_subscription_creation": True  # Key part!
        }

        created_plan = razorpay_client.plan.create(plan_data)
        return {
            "message": "Plan created successfully",
            "plan_id": created_plan["id"],
            "details": created_plan
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Razorpay error: {str(e)}")
