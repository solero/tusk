from fastapi import Request, Response
from tusk.api.app import app
from tusk.api.errors import WNSException
from tusk.api.routes import api
from tusk.handlers import get_package_modules

from tusk.data.ninja import CardCollection

from tusk.data import db
from redis import asyncio as aioredis

import tusk.places
import tusk.handlers

import os

app.include_router(api)

@app.exception_handler(WNSException)
async def wns_exception_handler(request: Request, exc: WNSException):
    return Response(
        content=f"[S_ERROR]|{exc.code}|{exc.title}||{exc.message}",
        media_type="text/plain"
    )

@app.on_event("startup")
async def startup_event():
    await db.set_bind(os.getenv("POSTGRES"))
    app.redis = aioredis.Redis(connection_pool=aioredis.ConnectionPool.from_url(os.getenv("REDIS")))
    app.places = {}
    app.server_futs = {}

    # load crumbs
    app.cards = CardCollection.get_collection()

    # load handlers
    get_package_modules(tusk.places)
    get_package_modules(tusk.handlers)

@app.get('/crossdomain.xml')
async def crossdomain():
    return Response(
        content="""
                    <cross-domain-policy>
                    <site-control permitted-cross-domain-policies="master-only"/>
                    <allow-access-from domain="*"/>
                    </cross-domain-policy>
                """,
        media_type="application/xml"
    )