from tusk.handlers import authenticated
from .constants import WINDOW_MANAGER_URL
from dataclasses import dataclass
from typing import Callable
import ujson
import inspect

window_handlers = {}


@dataclass
class WindowCommandObj:
    command: str
    callback: Callable

def window_event(cmd):
    def decorate(fn):
        async def callback(p, *args, **kwargs):
            if inspect.iscoroutinefunction(fn):
                await fn(p, *args, **kwargs)
            else:
                fn(p, *args, **kwargs)
        window_handlers[cmd] = window_handlers.get(cmd, [])
        window_handlers[cmd].append(WindowCommandObj(
            command=cmd,
            callback=callback
        ))
        return fn
    return decorate


class WindowManager:

    def __init__(self, p):
        self.penguin = p
        self.object_id = 101 + int(p.crossworld_ui)
        self.command = 'soleroTuskFramework'
        p.user_events[self.command] = [WindowCommandObj(command=None, callback=authenticated(self.received_from_framework))] #FIXME: not the best idea but works.

    async def load(self):
        await self.penguin.send_tag('UI_CROSSWORLDSWFREF', self.object_id, 0, 'WindowManagerSwf', 
                         0, 0, 0, 0, 0,
                         self.penguin.get_url(WINDOW_MANAGER_URL),
                         self.command
                         )
        await self.penguin.send_tag('UI_ALIGN', self.object_id, 0, 0, 'center', 'scale_none')

    async def send_action(self, action):
        await self.penguin.send_tag('UI_CLIENTEVENT', self.object_id, 'receivedJson', action.json(by_alias=True))

    async def received_from_framework(self, p, *data):
        data = ujson.loads(' '.join(data))
        handlers = window_handlers.get(data['triggerName'])

        if handlers is None:
            p.server.logger.warn(f"Window Handler {data['triggerName']} has no handlers!")
            return 
        
        for handler in handlers:
            try:
                await handler.callback(p, **data)
            except Exception as e:
                print(e)
                #TODO: PROPER ERROR HANDLING
                pass
