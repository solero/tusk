from . import PlaceObject
from tusk.places.objects import Tile


@PlaceObject('0:7940006')
class EmptyTileLobby(Tile):
    name: str = "Empty Tile"

@PlaceObject('0:7940007')
class BlankBlueLobby(Tile):
    name: str = "blankblue"

@PlaceObject('0:7940008')
class BlankGreenLobby(Tile):
    name: str = "blankgreen"

@PlaceObject('0:7940009')
class BlankGreyLobby(Tile):
    name: str = "blankgrey"

@PlaceObject('0:7940010')
class BlankPurpleLobby(Tile):
    name: str = "blankpurpl"

@PlaceObject('0:7940011')
class BlankWhiteLobby(Tile):
    name: str = "blankwhite"


