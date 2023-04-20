from tusk.handlers import server_command, slash_command, authenticated
from tusk.places.snow.windowmanager import window_event
from tusk.places.snow import OnPlaceId
from tusk.places.snow.models.card import PlayerSelectPayload, Element
from tusk.places.snow.models.window import SetWorldIdAction, SetBaseAssetUrlAction, SetFontPathAction, SkinRoomToRoomAction, LoadWindowAction
from tusk.places.snow.constants import LOADING_SCREEN_ASSETS, SNOW_ERROR_HANDLER, SNOW_PLAYER_SELECT
from tusk.places.snow.scripts import match_making


@window_event('windowManagerReady')
@OnPlaceId('0:0')
async def window_manager_ready(p, **_):
    await p.window_manager.send_action(SetWorldIdAction(
        world_id=p.server.id
    ))
    await p.window_manager.send_action(SetBaseAssetUrlAction(
        base_asset_url=p.get_url()
    ))
    await p.window_manager.send_action(SetFontPathAction(
        default_font_path=p.get_url('/fonts/')
    ))
    await p.window_manager.send_action(SkinRoomToRoomAction(
        url=p.get_url(LOADING_SCREEN_ASSETS)
    ))
    await p.window_manager.send_action(LoadWindowAction(
        window_url=p.get_url(SNOW_ERROR_HANDLER),
    ))

    await p.window_manager.send_action(LoadWindowAction(
        window_url=p.get_url(SNOW_PLAYER_SELECT),
        initialization_payload=PlayerSelectPayload(
            name=p.user.nickname, #TODO: check for username approval.
            power_cards_fire=len(p.cards['f']),
            power_cards_water=len(p.cards['w']),
            power_cards_snow=len(p.cards['s'])
        )
    ))

@slash_command('place_ready')
@OnPlaceId('0:0')
@authenticated
async def place_ready(p):
    player_object = await p.objects.create_object(x=5, y=2.5)
    await p.send_tag('P_CAMERA', 4.5, 2.5, 0, 0, 1)
    await p.send_tag('P_ZOOM', 1)
    await p.send_tag('P_LOCKZOOM', 1)
    await p.send_tag('P_LOCKCAMERA', 1)
    await player_object.set_as_camera_target()



@window_event('mmElementSelected')
@OnPlaceId('0:0')
async def handle_select_element(p, tipMode=True, element=None, **_):
    p.context['tipMode'] = tipMode
    element = getattr(Element, element.upper(), Element.FIRE)
    await match_making.add_to_queue(p, element)


@server_command('disconnected')
@authenticated
async def handle_disconnect(p):
    match_making.remove_from_queue(p)

@window_event('mmCancel')
@OnPlaceId('0:0')
async def handle_remove_from_matchmaking(p, **_):
    match_making.remove_from_queue(p)

