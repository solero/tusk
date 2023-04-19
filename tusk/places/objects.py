from .constants import TileModes

#[id (dynamic), url, blocking, blend, unused, unused, name, tile_mode, friction, bounce, sprite_id]

class Tile:
    url: str = ''
    blocking: bool = False
    blend: bool = False
    name: str = ''
    tile_mode: int = TileModes.STEPPED
    friction: bool = False
    bounce: bool = False
    sprite_id: str = "-1:-1"