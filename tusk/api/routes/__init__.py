from fastapi import APIRouter, Response
from tusk.api.routes.wns import world_name_service

api = APIRouter(
    '/api'
)
api.include_router(world_name_service)

@api.get('/ping')
async def wns_ping(timestamp: int, request_number: int):
    return Response(
        content=f"[WNS_PING]|{timestamp}|{request_number}",
        media_type='text/plain'
    )