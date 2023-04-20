from . import PlaceObject, PlacePreloadObject
from tusk.places.objects import Tile, Sprite


@PlaceObject
class EmptyTileLobby(Tile):
    name: str = "Empty Tile"
    art_index: str = '0:7940006'

@PlaceObject
class BlankBlueLobby(Tile):
    name: str = "blankblue"
    art_index: str = '0:7940007'

@PlaceObject
class BlankGreenLobby(Tile):
    name: str = "blankgreen"
    art_index: str = '0:7940008'

@PlaceObject
class BlankGreyLobby(Tile):
    name: str = "blankgrey"
    art_index: str = '0:7940009'

@PlaceObject
class BlankPurpleLobby(Tile):
    name: str = "blankpurpl"
    art_index: str = '0:7940010'

@PlaceObject
class BlankWhiteLobby(Tile):
    name: str = "blankwhite"
    art_index: str = "0:7940011"

@PlaceObject
class EmptyTile(EmptyTileLobby):
    art_index: str = '0:7940012'

@PlaceObject
class OpenTile(Tile):
    name: str = "open"
    art_index: str = '0:7940013'

@PlaceObject
class EnemyTile(Tile):
    name: str = "enemy"
    art_index: str = '0:7940014'

@PlaceObject
class PenguinTile(Tile):
    name: str = "penguin"
    art_index: str = '0:7940015'

@PlaceObject
class PenguinSpawnOccupiedTile(Tile):
    name: str = "penguin_spawn_occupied"
    art_index: str = '0:7940016'

@PlaceObject
class PenguinSpawnUnoccupiedTile(Tile):
    name: str = "penguin_spawn_unoccupied"
    art_index: str = '0:7940017'

@PlaceObject
class EnemySpawnOccupiedTile(Tile):
    name: str = "enemy_spawn_unoccupied"
    art_index: str = '0:7940018'

@PlaceObject
class EnemySpawnUnoccupiedTile(Tile):
    name: str = "enemy_spawn_occupied"
    art_index: str = '0:7940019'

@PlaceObject
class Obstacle(Tile):
    name: str = "obstacle"
    art_index: str = '0:7940020'


@PlaceObject
@PlacePreloadObject
class SlyMove(Sprite):
    art_index: str = "0:100307"

@PlaceObject
@PlacePreloadObject
class ScrapMove(Sprite):
    art_index: str = "0:100319"
    
@PlaceObject
@PlacePreloadObject
class TankMove(Sprite):
    art_index: str = "0:100303"

@PlaceObject
@PlacePreloadObject
class SlyHit(Sprite):
    art_index: str = "0:100308"

@PlaceObject
@PlacePreloadObject
class ScrapHit(Sprite):
    art_index: str = "0:100318"
    
@PlaceObject
@PlacePreloadObject
class SlyAttack(Sprite):
    art_index: str = "0:100306"
    
@PlaceObject
@PlacePreloadObject
class SlyProjectile(Sprite):
    art_index: str = "0:100310"

@PlaceObject
@PlacePreloadObject
class ScrapAttack(Sprite):
    art_index: str = "0:100312"

@PlaceObject
@PlacePreloadObject
class ScrapProjectileEast(Sprite):
    art_index: str = "0:100315"

@PlaceObject
@PlacePreloadObject
class ScrapProjectileNorth(Sprite):
    art_index: str = "0:100316"

@PlaceObject
@PlacePreloadObject
class ScrapHit(Sprite):
    art_index: str = "0:100317"

@PlaceObject
@PlacePreloadObject
class ScrapAttackEffect(Sprite):
    art_index: str = "0:100313"

@PlaceObject
@PlacePreloadObject
class ScrapAttackLittleEffect(Sprite):
    art_index: str = "0:100314"

@PlaceObject
@PlacePreloadObject
class TankHit(Sprite):
    art_index: str = "0:100302"

@PlaceObject
@PlacePreloadObject
class TankAttack(Sprite):
    art_index: str = "0:100299"

@PlaceObject
@PlacePreloadObject
class TankSwipeHorizontal(Sprite):
    art_index: str = "0:100240"

@PlaceObject
@PlacePreloadObject
class TankSwipeVertical(Sprite):
    art_index: str = "0:100241"

@PlaceObject
@PlacePreloadObject
class SlyKo(Sprite):
    art_index: str = "0:100309"

@PlaceObject
@PlacePreloadObject
class ScrapKo(Sprite):
    art_index: str = "0:100320"

@PlaceObject
@PlacePreloadObject
class TankKo(Sprite):
    art_index: str = "0:100304"

@PlaceObject
@PlacePreloadObject
class SlyDaze(Sprite):
    art_index: str = "0:1840011"

@PlaceObject
@PlacePreloadObject
class ScrapDaze(Sprite):
    art_index: str = "0:1840012"

@PlaceObject
@PlacePreloadObject
class TankDaze(Sprite):
    art_index: str = "0:1840010"

@PlaceObject
class TankDaze(Sprite):
    art_index: str = "0:1840010"
