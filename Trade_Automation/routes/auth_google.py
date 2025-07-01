from fastapi import APIRouter, Request,Depends
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from core.config import settings
from core.database import get_db
from services.user import google_auth_user
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()
oauth = OAuth()

# Register Google OAuth2
oauth.register(
    name='google',
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={'scope': 'openid email profile'},
)

@router.get("/auth/google")
async def login_via_google(request: Request):
    redirect_uri = "http://localhost:8000/auth/google/callback"
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/auth/google/callback", name="auth_google_callback")
async def auth_google_callback(request: Request, db: AsyncSession = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    jwt_token = await google_auth_user(email=user_info["email"], full_name=user_info.get("name"), db=db)

    return {"access_token": jwt_token, "token_type": "bearer"}
