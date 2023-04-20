from typing import Any, Callable
from dataclasses import dataclass
import inspect
import pkgutil
import importlib

slash_command_handlers = {}
server_handlers = {}


def get_package_modules(package):
    package_modules = []
    for importer, module_name, is_package in pkgutil.iter_modules(package.__path__):
        full_module_name = f'{package.__name__}.{module_name}'
        subpackage_object = importlib.import_module(full_module_name, package=package.__path__)
        if is_package:
            sub_package_modules = get_package_modules(subpackage_object)

            package_modules = package_modules + sub_package_modules
        package_modules.append(subpackage_object)
    return package_modules



@dataclass
class SlashCommandObj:
    command: str
    callback: Callable

def slash_command(cmd, place=None):
    def decorate(fn):
        async def callback(p, *args):
            if place is not None and p.place.name != place:
                return
            if inspect.iscoroutinefunction(fn):
                await fn(p, *args)
            else:
                fn(p, *args)
        slash_command_handlers[cmd] = slash_command_handlers.get(cmd, [])
        slash_command_handlers[cmd].insert(0, SlashCommandObj(
            command=cmd,
            callback=callback
        ))
        return fn
    return decorate
    
def authenticated(fn):
    async def handle(p, *args):
        if not p.user:
            return p.close()
        return await fn(p, *args)
    return handle


def server_command(evt):
    def decorate(fn):
        async def callback(*args):
            if inspect.iscoroutinefunction(fn):
                await fn(*args)
            else:
                fn(*args)
        server_handlers[evt] = server_handlers.get(evt, [])
        server_handlers[evt].insert(0, callback)
        return fn
    return decorate
    

