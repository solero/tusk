from tusk.places import DefaultWorld, Place, Input, Object, PreloadObject
import base64

def read_tilemap(filename):
    with open(f"./tusk/places/snow/maps/{filename}.png", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def PlaceInput(input_obj):
    return Input('snow_lobby', input_obj)

def PlaceObject(cls):
    return Object('snow_lobby')(cls)

def PlacePreloadObject(cls):
    PreloadObject('snow_lobby')(cls)
    return cls

def OnPlaceId(place_id: str):
    def decorate(fn):
        async def handle(p, *args, **kwargs):
            if p.place.place_id != place_id:
                return
                
            return await fn(p, *args, **kwargs)
        return handle
    return decorate


@Place('0:0', 1, 0, 'snow_lobby')
class SnowLobby(DefaultWorld):
    class PlaceSettings(DefaultWorld.PlaceSettings):

        class MapBlocks:
            tile: str = read_tilemap('tilemap')
            height: str = read_tilemap('heightmap')

        class Camera(DefaultWorld.PlaceSettings.Camera):
            tile_size: int = 100
            elevation_scale: float = 0.031250
        tile_list: list = ['0:7940006', '0:7940007', '0:7940008', '0:7940009', '0:7940010', '0:7940011']
        
@Place('0:10001', 8, 1, 'snow_lobby')
class SnowBattle(SnowLobby):
    class PlaceSettings(SnowLobby.PlaceSettings):
        tile_list: list = ['0:7940012', '0:7940013', '0:7940014', '0:7940015', '0:7940016', '0:7940017', '0:7940018', '0:7940019', '0:7940020']
    