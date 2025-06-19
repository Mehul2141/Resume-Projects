from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.security import get_current_user
from core.config import settings
from models import User
from services.user_broker import save_user_broker as add_broker
from services.brokers.angelone import get_client_code
import datetime


API_KEY = settings.ANGELONE_API_KEY
REDIRECT_URI = settings.ANGELONE_REDIRECT_URI



router = APIRouter(prefix="/broker", tags=["Broker Integration"])

@router.get("/angelone/connect", summary="Start Angel One Publisher Login")
def connect_angelone(db: AsyncSession = Depends(get_db)):
    if not API_KEY:
        raise HTTPException(status_code=500, detail="ANGEL_PUBLISHER_API_KEY not configured")
    login_url = (
        "https://smartapi.angelbroking.com/publisher-login"
        f"?api_key={API_KEY}"
        f"&redirect_uri={REDIRECT_URI}"
    )
    return RedirectResponse(login_url)

@router.get("/angelone/callback", summary="Start Angel One Publisher redirect")
async def callback_angelone(
    request: Request,
    db: AsyncSession = Depends(get_db)
):
    jwt_token = request.query_params.get("auth_token")
    refresh_token = request.query_params.get("refresh_token")
    feed_token = request.query_params.get("feed_token")
    broker_name = "Angle-one"
    #user_id = current_user.user_id

    if not all([jwt_token, refresh_token, feed_token]):
        raise HTTPException(status_code=400, detail="Missing required tokens")
    
    client_code = get_client_code(jwt_token=jwt_token, refresh_token=refresh_token)
    print(f"client code: {client_code}")

    expires_at = datetime.datetime.utcnow() + datetime.timedelta(days=1)
    created_at = datetime.datetime.utcnow()

    await add_broker(
        db=db,
        user_id="user_id",
        broker_name=broker_name,
        client_code=client_code,
        jwt_token=jwt_token,
        refresh_token=refresh_token,
        feed_token=feed_token,
        expires_at=expires_at,
        created_at=created_at,
    )

    return {"message": "Broker details saved successfully"}