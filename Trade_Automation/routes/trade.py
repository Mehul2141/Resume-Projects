from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from models.trade import Trade
from core import auth
from schemas.trade import JWTBearer, ResponseSchema
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


router = APIRouter(prefix="/trade", tags=["Trades"])
security = HTTPBearer()

@router.get("/")
async def get_trades(credentials: HTTPAuthorizationCredentials = Depends(security), db: AsyncSession = Depends(get_db)):
    # Check if trades exists
    access_token = credentials.credentials
    user_details = auth.decode_token(access_token)
    user_id = user_details["sub"]
    print(f"user details: {user_id}")
    try:
        result = await db.execute(select(Trade).where(Trade.user_id == user_id))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # if not result.scalars().all():
    #         raise HTTPException(status_code=404, detail="No trades found.")
    trades = result.scalar_one_or_none()
    print(f"type of response: {type(trades)}")
    return trades