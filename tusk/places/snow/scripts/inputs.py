from tusk.places.snow import PlaceInput
from tusk.places import InputObj
from tusk.places.constants import MouseTarget, InputModifier, InputEvent


@PlaceInput(InputObj(
    input_id = "use",
    script_id = "0:10",
    target = MouseTarget.GAME_OBJECT,
    modifier = InputModifier.NONE,
    command = "use"
))
async def game_object_selected(p, object_id, x, y, obj_x, obj_y):
    # TO DO: Handle Game Object Clicking
    pass
