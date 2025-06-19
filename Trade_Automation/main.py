from fastapi import FastAPI
from fastapi.security import HTTPBearer
from routes import user as auth_routes
from routes import trade as trade_routes
from routes import user_broker as broker_routes
import models

#bearer_scheme = HTTPBearer()
app = FastAPI()

app.include_router(auth_routes.router)
app.include_router(trade_routes.router)
app.include_router(broker_routes.router)