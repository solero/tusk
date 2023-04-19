from enum import IntEnum

class ViewMode(IntEnum):
    TOP = 0
    TOP_ROTATED = 1
    STEPPED = 2
    SLOPED = 3
    FLAT_ISO = 4
    SIDE = 5
    CAMERA = 6
    
class MouseTarget(IntEnum):
    GAME_TILE = 1
    GAME_OBJECT = 2
    
class InputModifier(IntEnum):
    NONE = 0
    SHIFT = 1
    CTRL = 2
    ALT = 3
    
class InputEvent(IntEnum):
    KEY_UP = 1
    KEY_DOWN = 2
    MOUSE_CLICK = 3
    MOUSE_BOX = 4
    MOUSE_DOUBLE_CLICK = 5
    MOUSE_UP = 12
    
class TileModes(IntEnum):
    SLOPED = 0
    STEPPED = 1