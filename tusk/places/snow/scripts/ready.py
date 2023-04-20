from tusk.handlers import slash_command, authenticated
from tusk.places.snow.windowmanager import WindowManager
from tusk.data.ninja import PenguinCardCollection
from tusk.api.app import app


@slash_command('set_crossworld_ui')
async def set_crossworld_ui(p, crossworld_ui):
    p.crossworld_ui = crossworld_ui == 1

@slash_command('ready')
@authenticated
async def ready(p):
    p.window_manager = WindowManager(p)
    await p.window_manager.load()

    p.cards = { 'f': [], 'w': [], 's': [] }
    power_cards = await PenguinCardCollection.get_collection(p.user.id)
    for penguin_card in power_cards:
        card = app.cards[penguin_card.card_id]
        p.cards[card.element].append(card)