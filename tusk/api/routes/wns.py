from fastapi import APIRouter, Depends, Response
from tusk.api.app import app
from tusk.api.errors import WNSException
from tusk.tusk import Tusk
import asyncio


def get_world_created(owner: str):
    i = 0
    for place in app.places.values():
        if place.owner == owner:
            i += 1
    return i

async def authenticate_session(token: str, owner: str):
    session = await app.redis.get(f'{owner}.mpsession')
    if session is None or session.decode() != token:
        raise WNSException(3525, 'Cannot Start World', 'invalid token')

world_name_service = APIRouter(
    prefix='/v0.2/xxx/game/get/world-name-service',
    dependencies=[Depends(authenticate_session)]
)

@world_name_service.get('/start_world_request')
async def start_world(name: str, owner: str, worlds_created: int = Depends(get_world_created)):
    world = app.places.get(name)
    world_destination = await app.redis.get(f'{owner}.mp.world')
    if world_destination is None:
        world_destination = await app.redis.set(f'{owner}.mp.world', '0:0') # 0:0 is lobby in this case.

    if world is None:
        if worlds_created > 0: # each user can only create one world/server to prevent ddosing, atleast i hope it would stop them.
            raise WNSException(3110, 'Cannot Start World', 'too many requests')
        elif len(app.places) > 100:
            raise WNSException(3516, 'Cannot Start World', 'no available servers')

        world = app.places[name] = Tusk(len(app.places), owner, name)
        await world.start()
        return Response(
            content=f"[S_WORLDSTATUS]|{name}|starting|Requested world startup|500"
        )
    
    return Response(
        content=f"[S_WORLDLIST]|{world.id}|{name}|127.0.0.1|{world.port}||{world.owner}|{name}|cp_cjsnow_trunk|{world.id}"
    )
    