from tusk.handlers import server_command
from tusk.api.app import app

@server_command('disconnected')
async def disconnected(p):
    if len(p.server.penguins_by_id) <= 0:
        p.server.server_coroutine.cancel()
        del app.places[p.server.id]
