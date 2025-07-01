from fastapi import FastAPI
from routes import user as auth_routes
from routes import trades
from routes import user_broker,user_strategies,user_subscription
from contextlib import asynccontextmanager
import asyncio
from routes.auth_google import router as google_auth_router
from starlette.middleware.sessions import SessionMiddleware
from core.config import settings  # contains your secret key



from fastapi.security import HTTPBearer

bearer_scheme = HTTPBearer()

from datafeeds.candle_builder import run
from datafeeds.websocket import sws
from fastapi.responses import JSONResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    loop = asyncio.get_event_loop()
    loop.run_in_executor(None, sws.connect)
    candle_task = asyncio.create_task(run())
    yield
    candle_task.cancel()
    sws.on_close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(SessionMiddleware, secret_key=settings.GOOGLE_CLIENT_SECRET)


app.include_router(auth_routes.router)
app.include_router(trades.router)
app.include_router(user_broker.router)
app.include_router(user_strategies.router)
app.include_router(user_subscription.router)
app.include_router(google_auth_router)

