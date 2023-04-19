from tusk.handlers import slash_command
from tusk.api.app import app
from tusk.data.penguin import Penguin
from tusk.places import get_place

async def authenticate_session(player_id: str, token: str):
    session = await app.redis.get(token)
    if session is None or session.decode() != player_id:
        return False
    return True

@slash_command('version')
async def handle_get_server_version(p):
    await p.send_tag('S_VERSION', 'FY15-20150206 (4954)r', 'Tusk', 'https://github.com/solero/tusk')

@slash_command('place_context')
async def handle_set_place_context(p, place: str, query_arg: str):
    # p.place = place.replace('"', '')
    pass

@slash_command('login')
async def handle_login(p, env, player_id, token):
    authenticated = await authenticate_session(player_id, token)
    await p.send_tag('S_LOGINDEBUG', 'Got /login command from user')
    if not authenticated:
        return await p.send_tag('S_LOGINDEBUG', 'user code 900')

    await p.send_tag('S_LOGINDEBUG', 'Successfully verified credentials server-side')
    p.user = await Penguin.get(int(player_id))
    world = await app.redis.get(f'{player_id}.mp.world')
    world = world.decode()
    p.place = get_place(world)
    await p.send_tag('S_LOGINDEBUG', 'Finalizing login, creating final user object')
    await p.send_tag('S_WORLDTYPE', 0, 1, 0)
    await p.send_tag('S_WORLD', p.server.id, p.server.name, '0:0', 0, 'none', 0, p.server.owner, p.server.name, 0, p.server.stylesheet_id, 0)
    await p.send_tag('S_LOGIN', p.user.id)
    await p.send_tag('W_BASEASSETURL')
    await p.send_tag('W_DISPLAYSTATE')
    await p.send_tag('W_ASSETSCOMPLETE', p.user.id)

#cjsnow_0f306f48-5ca3-49a1-b423-3990d81c355a|0:0|0|none|0|{0f306f48-5ca3-49a1-b423-3990d81c355a}|cjsnow_0f306f48-5ca3-49a1-b423-3990d81c355a|0|87.5309|0