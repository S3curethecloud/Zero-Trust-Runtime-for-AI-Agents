from __future__ import annotations

from fastapi import FastAPI

from aib_api.routes.health import router as health_router
from aib_api.routes.token import router as token_router
from aib_api.routes.sessions import router as sessions_router
from aib_api.routes.introspect import router as introspect_router


app = FastAPI(title="Agent Identity Broker (AIB)", version="0.1.0")

app.include_router(health_router)
app.include_router(token_router)
app.include_router(introspect_router)
app.include_router(sessions_router)
