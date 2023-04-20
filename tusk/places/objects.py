from .constants import TileModes

#[id (dynamic), url, blocking, blend, unused, unused, name, tile_mode, friction, bounce, sprite_id]


class Template:
    art_index: str = "0:1"

class Sprite:
    art_index: str = "-1:-1"

class Tile(Sprite):
    url: str = ''
    blocking: bool = False
    blend: bool = False
    name: str = ''
    tile_mode: int = TileModes.STEPPED
    friction: bool = False
    bounce: bool = False
