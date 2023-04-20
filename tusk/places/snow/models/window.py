from tusk.places.snow.models import CamelCaseModel
from typing import Any

class WindowAction(CamelCaseModel):
    action: str = ''
    type: str = ''

class ImmediateAction(WindowAction):
    type: str = 'immediateAction'

class PlayAction(WindowAction):
    type: str = 'playAction'

class SetWorldIdAction(ImmediateAction):
    action: str = 'setWorldId'
    world_id: int

class SetBaseAssetUrlAction(ImmediateAction):
    action: str = 'setBaseAssetUrl'
    base_asset_url: str

class SetFontPathAction(ImmediateAction):
    action: str = 'setFontPath'
    default_font_path: str

class JsonPayloadAction(ImmediateAction):
    action: str = 'jsonPayload'
    json_payload: Any
    target_window: str
    trigger_name: str

class CloseCjsnowRoomToRoomAction(ImmediateAction):
    action: str = 'closeCjsnowRoomToRoom'
    target_window: str = 'cardjitsu_snowplayerselect.swf'

class SkinRoomToRoomAction(PlayAction):
    action: str = 'skinRoomToRoom'
    url: str
    class_name: str = ""
    variant: int = 0

class LoadWindowAction(PlayAction):
    action: str = 'loadWindow'
    assetPath: str = ''
    initialization_payload: Any = [None]
    layer_name: str = 'bottomLayer'
    load_description: str = ''
    window_url: str
    x_percent: int = 0
    y_percent: int = 0

class CloseWindowAction(PlayAction):
    action: str = 'closeWindow'
    target_window: str

