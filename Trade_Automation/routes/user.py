from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from core.database import get_db
from models.user import User
from core import auth
from schemas.user import RegisterSchema, LoginSchema, TokenResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=TokenResponse)
async def register(payload: RegisterSchema, db: AsyncSession = Depends(get_db)):
    # Check if email already exists
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        mobile=payload.mobile,
        password=auth.hash_password(payload.password),
        role="User"
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = auth.create_access_token(data={"sub": str(new_user.user_id)})
    return {"access_token": token}

@router.post("/login", response_model=TokenResponse)
async def login(payload: LoginSchema, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not auth.verify_password(payload.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password.")

    token = auth.create_access_token(data={"sub": str(user.user_id)})
    return {"access_token": token}