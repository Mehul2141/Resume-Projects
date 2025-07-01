from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.user import User
from core import auth
from schemas.user import RegisterSchema, LoginSchema
from fastapi import HTTPException

async def register_user(payload: RegisterSchema, db: AsyncSession) -> str:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(status_code=400, detail="Email already registered.")

    new_user = User(
        full_name=payload.full_name,
        email=payload.email,
        mobile=payload.mobile,
        password=auth.hash_password(payload.password),
        role=payload.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    token = auth.create_access_token(data={"sub": str(new_user.user_id)})
    return token


async def authenticate_user(payload: LoginSchema, db: AsyncSession) -> str | None:
    result = await db.execute(select(User).where(User.email == payload.email))
    user = result.scalar_one_or_none()
    if not user or not auth.verify_password(payload.password, user.password):
        return None

    token = auth.create_access_token(data={"sub": str(user.user_id)})
    return token


async def google_auth_user(email: str, full_name: str, db: AsyncSession) -> str:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalar_one_or_none()

    if not user:
        user = User(
            full_name=full_name,
            email=email,
            mobile=None,  # optional for Google users
            password=None,
            role="user",
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)

    token = auth.create_access_token(data={"sub": str(user.user_id)})
    return token

