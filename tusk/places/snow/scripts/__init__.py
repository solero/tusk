from tusk.places.snow.models.card import Element
from tusk.places.snow.models.window import JsonPayloadAction, CloseWindowAction
from tusk.places.snow.constants import SNOW_PLAYER_SELECT
from urllib.parse import urlencode
import asyncio

class CJSMatchMaking:

    def __init__(self):
        self.players = {
            Element.FIRE: [],
            Element.WATER: [],
            Element.SNOW: []
        }
    
    async def add_to_queue(self, p, element):
        p.element = element
        self.players[element].append(p)
        if all([len(players) > 0 for players in self.players.values()]):
            players = []
            payload = {}
            for element in self.players:
                player = self.players[element].pop(0)
                payload[str(int(element))] = player.user.nickname # TODO: check for name approval.
                players.append(player)
            for player in players:
                await player.window_manager.send_action(JsonPayloadAction(
                    json_payload = payload,
                    target_window = player.get_url(SNOW_PLAYER_SELECT),
                    trigger_name = 'matchFound'
                ))
            await asyncio.sleep(3)
            await self.send_players_to_battle(players)

    async def send_players_to_battle(self, players):
        for player in players:
            await player.window_manager.send_action(CloseWindowAction(
                target_window = player.get_url(SNOW_PLAYER_SELECT)
            ))
            async with player.server.redis.pipeline(transaction=True) as pipe:
                await (pipe.set(f'{player.user.id}.element', int(player.element))
                            .set(f'{player.user.id}.mp.world', '0:10001').execute()) # 0:10001 is the snow battle world id.
            await player.send_tag('S_GOTO', f'cjsnow_{players[0].user.id}', 'snow_lobby', '', urlencode(player.context)) # send to the battling server.

    async def remove_from_queue(self, player):
        if player.element is None:
            return
        if player in self.players[player.element]:
            self.players[player.element].remove(player)

match_making = CJSMatchMaking()