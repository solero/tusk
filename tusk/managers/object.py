from dataclasses import dataclass, field
from tusk.places.objects import Sprite
from typing import Any, Callable, Dict
import weakref

@dataclass
class Object:
    manager: Any
    id: int
    art: str = '0:1'
    x: int = 0
    y: int = 0
    z: int = 0
    name: str = ''
    template: str = '0:1'
    block: bool = False
    pickable: bool = False
    scale_by_depth: bool = False
    callbacks: Dict = field(default_factory=dict)

    async def init(self):
        await self.manager.penguin.send_tag('O_HERE', self.id, self.art, 
                                            self.x, self.y, self.z, int(not self.z),
                                            0, 0, 0, self.name, self.template, int(self.block), int(self.pickable), int(self.scale_by_depth))

    async def move(self, x, y, z=0):
        self.x, self.y, self.z = x, y, z
        await self.manager.penguin.send_tag('O_MOVE', self.id, x, y, z)

    async def animate(self, sprite: Sprite, play_style='play_once', time_scale: int = 1, no_reset: bool = False, callback: Callable = None):
        handle_id = self.manager.handle_id
        if callback is not None:
            self.callbacks[handle_id] = callback
        await self.manager.penguin.send_tag('O_ANIM', self.id, sprite.art_index, play_style, 
                                            sprite.duration, time_scale, int(no_reset), self.id, handle_id)

    async def animate_sprite(self, start_frame=0, end_frame=0, backwards=False, play_style='play_once', duration=None):
        await self.manager.penguin.send_tag('O_SPRITEANIM', self.id, start_frame, end_frame, int(backwards), play_style, duration or '')

    async def update_sprite(self, sprite: Sprite, frame: int = 0, relative_path: str = ''):
        await self.manager.penguin.send_tag('O_SPRITE', self.id, sprite.art_index, frame, relative_path)

    async def set_as_camera_target(self):
        await self.manager.penguin.send_tag('O_PLAYER', self.id)

    async def delete(self):
        await self.manager.penguin.send_tag('O_GONE', self.id)

class ObjectManager:

    def __init__(self, penguin):
        self.penguin = penguin
        self._handle_id = 0
        self._game_object_id = 0
        self.objects = {}
        self.ref = weakref.proxy(self)
    
    @property
    def game_object_id(self):
        self._game_object_id += 1
        return self._game_object_id
    
    @property
    def handle_id(self):
        self._handle_id += 1
        return self._handle_id
    
    def get_object(self, obj_id):
        return self.objects.get(obj_id)

    async def create_object(self, art: str = '0:1', x: int = 0, y: int = 0 , z: int = 0, 
                            name: str = '', template: str = '0:1', block: bool = False, pickable: bool = False,
                            scale_by_depth: bool = False
                            ):
        obj_id = self.game_object_id
        obj = self.objects[obj_id] = Object(self.ref, obj_id, art, x, y, z, name, template, block, pickable, scale_by_depth)
        await obj.init()
        return obj

