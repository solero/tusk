from tusk.places.snow.models import CamelCaseModel
from enum import IntFlag, auto

class Element(IntFlag):
    FIRE = auto()
    SNOW = auto()

class PlayerSelectPayload(CamelCaseModel):
    game: str = "snow"
    name: str
    power_cards_fire: int = 0
    power_cards_snow: int = 0
    power_cards_water: int = 0

class PowerCard(CamelCaseModel):
    asset: str = ""
    card_id: int 
    color: str 
    description: str
    element: str
    is_active: bool = True
    label: str
    name: str
    power_id: int
    prompt: str
    set_id: int
    value: int