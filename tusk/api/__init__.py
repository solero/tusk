from fastapi import Request, Response
from tusk.api.app import app
from tusk.api.errors import WNSException
from tusk.data import db
from redis import asyncio as aioredis

import os

@app.exception_handler(WNSException)
async def mws_exception_handler(request: Request, exc: WNSException):
    return Response(
        content=f"[S_ERROR]|{exc.code}|{exc.title}||{exc.message}",
        media_type="text/plain"
    )

@app.on_event("startup")
async def startup_event():
    await db.set_bind(os.getenv("POSTGRES"))
    app.redis = aioredis.ConnectionPool.from_url(os.getenv("REDIS"))
    app.places = {}
    app.server_futs = {}