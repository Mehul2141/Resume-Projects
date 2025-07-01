from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from schemas.user import RegisterSchema, LoginSchema, TokenResponse
from services.user import register_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterSchema, db: AsyncSession = Depends(get_db)):
    token = await register_user(payload, db)
    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginSchema, db: AsyncSession = Depends(get_db)):
    token = await authenticate_user(payload, db)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid email or password.")
    return {"access_token": token}


