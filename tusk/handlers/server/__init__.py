from tusk.handlers import server_command, authenticated
from tusk.api.app import app
import asyncio

def destroy_server(server):
    if len(server.penguins_by_id) <= 0:
        server.logger.info(f"Shutting down {server.name}")
        server.server_coroutine.cancel()
        server.logger.handlers.clear()
        del app.places[server.name]

@server_command('disconnected')
@authenticated
async def disconnected(p):
    destroy_server(p.server)

@server_command('boot')
async def handle_boot(server):
    loop = asyncio.get_running_loop()
    # 5 minutes until server auto shuts down
    loop.call_later(300, destroy_server, server)