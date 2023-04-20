from tusk.places.constants import ViewMode
from dataclasses import dataclass
from typing import Any, Callable, Optional
import inspect

inputs = {}
preloaded_objects = {}
_objects = {}
places = {}

def Object(place):
    def decorate(cls):
        _objects[place] = _objects.get(place, {})
        _objects[place][cls.art_index] = cls
        return cls
    return decorate
    
def get_object(place, art_index):
    return _objects[place][art_index]
    
def PreloadObject(place):
    def decorate(cls):
        preloaded_objects[place] = preloaded_objects.get(place, [])
        preloaded_objects[place].append(cls)
        return cls
    return decorate
    
def get_preload_objects(place):
    return preloaded_objects.get(place, [])
    

@dataclass
class InputObj:
    input_id: str
    script_id: str
    target: int
    event: int
    modifier: int
    command: str
    callback: Optional[Callable] = None

    
def Input(place: str, obj: InputObj):
    def decorate(fn: Callable):
        async def callback(*args):
            if inspect.iscoroutinefunction(fn):
                await fn(*args)
            else:
                fn(*args)
        obj.callback = callback
        inputs[place] = inputs.get(place, {})
        inputs[place][obj.command] = obj
        return fn
    return decorate

def get_inputs(place):
    return inputs[place]

@dataclass
class PlaceObj:
    place_id: str
    object_id: str
    instance_id: str
    name: str
    cls: Any


def Place(place_id, object_id, instance_id, name):
    def decorate(cls):
        places[place_id] = PlaceObj(
            place_id,
            object_id,
            instance_id,
            name,
            cls
        )
        return cls
    return decorate

def get_place(place):
    return places[place]

class DefaultWorld:
    
    class PlaceSettings:

        class MapBlocks:
            tile: str = ""
            height: str = ""

        class ZoomLimit:
            x: int = -1
            y: int = -1
        
        class Render:
            occluding_tiles: bool = False
            alpha_cutoff: int = 48
        
        class Camera:
            view_mode: int = int(ViewMode.SIDE)
            lock_view: bool = False
            tile_size: int = 64
            elevation_scale: float = -1
            terrain_lighting: bool = True
            
            # P_LOCKSCROLL
            lock_scroll: bool = True
            move_radius: int = 0
            move_rate: int = 0
            move_recenter: int = 0
            
            #P_HEIGHTMAPDIVISIONS
            height_map_divisions: int = 1
            
            #P_CAMLIMITS
            margin_top_left_x: int = 0
            margin_top_left_y: int = 0
            margin_bottom_right_x: int = 0
            margin_bottom_right_y: int = 0
        
        class Camera3D:
            near: int = 0
            far: int = 0
            position: list = [0, 0, 0]
            angle: list = [0, 0, 0]
            camera_view: int = 0
            left: int = 0
            right: int = 0
            top: int = 0
            bottom: int = 0
            aspect: int = 0
            v_fov: int = 0
            focal_length: int = 864397819904
            unknown: int = 0
            camera_width: int = 1024
            camera_height: int = 768
        
        class Physics:
            gravity: bool = False
            collision: bool = False
            friction: bool = False
            tile_friction: bool = False
            safety_net: bool = False
            net_height: int = 0
            net_friction: bool = False
            net_bounce: bool = True
            
        draggable: bool = False
        object_lock: bool = False
        tile_list: list = []
        
    class UISettings:
        background_color: list = [0, 0, 0]
        class BackgroundSprite:
            sprite_id: str = "0:-1"
            fit_type: int = 0
            scale_x: int = 1
            scale_y: int = 1