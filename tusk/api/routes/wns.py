from fastapi import APIRouter, Depends, Response
from tusk.api.app import app
from tusk.api.errors import WNSException
from tusk.tusk import Tusk
import asyncio


async def authenticate_session(token: str):
    session = await app.redis.get(f'{token}')
    if session is None or session.decode() != token:
        raise WNSException(3525, 'Cannot Start World', 'invalid token')

world_name_service = APIRouter(
    '/v0.2/xxx/game/get/world-name-service',
    dependencies=[Depends(authenticate_session)]
)

@world_name_service.get('/start_world_request')
async def start_world(name: str, owner: str):
    world = app.places.get(name)
    if world is None:
        world = app.places[name] = Tusk(len(app.places), owner, name)
        app.server_futs[name] = asyncio.create_task(world.start())
        return Response(
            content=f"[S_WORLDSTATUS]|{name}|starting|Requested world startup|500"
        )
    
    return f"[S_WORLDLIST]|{world.id}|{name}|127.0.0.1|{world.port}||{world.owner}|{name}|cp_cjsnow_trunk|{world.id}"
    