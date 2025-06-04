from fastapi import FastAPI
from routes import user as auth_routes
from routes import trade as trade_routes
import models

app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(trade_routes.router)