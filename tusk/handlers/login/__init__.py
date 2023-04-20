from tusk.handlers import slash_command
from tusk.api.app import app
from tusk.data.penguin import Penguin
from tusk.places import get_place

from urllib.parse import parse_qs

async def authenticate_session(player_id: int, token: str):
    session = await app.redis.get(f'{player_id}.mpsession')
    if session is None or session.decode() != token:
        return False
    return True

@slash_command('version')
async def handle_get_server_version(p):
    await p.send_tag('S_VERSION', 'FY15-20150206 (4954)r', 'Tusk', 'https://github.com/solero/tusk')

@slash_command('place_context')
async def handle_set_place_context(p, place: str, query_arg: str):
    query_string = parse_qs(query_arg)
    for context_key, context_val in query_string.items():
        p.context[context_key] = context_val[0]

@slash_command('login')
async def handle_login(p, env, player_id, token):
    player_id = int(player_id)
    authenticated = await authenticate_session(player_id, token)
    await p.send_tag('S_LOGINDEBUG', 'Got /login command from user')
    if not authenticated:
        return await p.send_tag('S_LOGINDEBUG', 'user code 900')
    await p.send_tag('S_LOGINDEBUG', 'Successfully verified credentials server-side')

    if player_id in p.server.penguins_by_id:
        return await p.send_tag('S_LOGGEDIN')
    
    p.user = await Penguin.get(player_id)
    p.server.penguins_by_id[p.user.id] = p
    await success_login(p)

@slash_command('force_login')
async def force_login(p):
    old_session = p.server.penguins_by_id.pop(p.user.id)
    p.server.penguins_by_id[p.user.id] = p # add the penguin into the penguins_by_id object to prevent it being deleted
    old_session.close()
    await success_login(p)

async def success_login(p):

    world = await app.redis.get(f'{p.user.id}.mp.world')
    await app.redis.delete(f'{p.user.id}.mp.world')

    world = world.decode()
    p.place = get_place(world)
    await p.send_tag('S_LOGINDEBUG', 'Finalizing login, creating final user object')
    

    await p.send_tag('S_WORLDTYPE', 0, 1, 0)
    await p.send_tag('S_WORLD', p.server.id, p.server.name, '0:0', 0, 'none', 0, p.server.owner, p.server.name, 0, p.server.stylesheet_id, 0)
    await p.send_tag('S_LOGIN', p.user.id)
    await p.send_tag('W_BASEASSETURL')
    await p.send_tag('W_DISPLAYSTATE')
    await p.send_tag('W_ASSETSCOMPLETE', p.user.id)