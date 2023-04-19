from tusk.handlers import slash_command, authenticated
from tusk.places import get_inputs, get_object

@slash_command('ready')
@authenticated
async def server_ready(p):
    inputs = get_inputs(p.place.name)
    for ipt in inputs:
        await p.send_tag('W_INPUT', ipt.input_id, ipt.script_id, ipt.target, ipt.modifier, ipt.command, '')
    await p.send_tag('W_PLACE', p.place.place_id, p.place.object_id, p.place.instance_id)

    place_class = p.place.cls

    await p.send_tag('P_MAPBLOCK', 't', 1, 1, place_class.PlaceSettings.MapBlocks.tile)
    await p.send_tag('P_MAPBLOCK', 'h', 1, 1, place_class.PlaceSettings.MapBlocks.height)
    await p.send_tag('P_ZOOMLIMIT', place_class.PlaceSettings.ZoomLimit.x, place_class.PlaceSettings.ZoomLimit.y)
    await p.send_tag('P_RENDERFLAGS', int(place_class.PlaceSettings.Render.occluding_tiles), place_class.PlaceSettings.Render.alpha_cutoff)

    camera_settings = place_class.PlaceSettings.Camera
    await p.send_tag('P_VIEW', camera_settings.view_mode)
    await p.send_tag('P_LOCKVIEW', int(camera_settings.lock_view))
    await p.send_tag('P_TILESIZE', camera_settings.tile_size)
    await p.send_tag('P_ELEVSCALE', camera_settings.elevation_scale)
    await p.send_tag('P_RELIEF', int(camera_settings.terrain_lighting))
    await p.send_tag('P_LOCKSCROLL', int(camera_settings.lock_scroll), camera_settings.move_radius, camera_settings.move_rate, camera_settings.move_recenter)
    await p.send_tag('P_HEIGHTMAPDIVISIONS', camera_settings.height_map_divisions)
    camera3d_settings = place_class.PlaceSettings.Camera3D
    await p.send_tag('P_CAMERA3D', camera3d_settings.near, camera3d_settings.far, 
                        *camera3d_settings.position, *camera3d_settings.angle, 
                        camera3d_settings.camera_view, camera3d_settings.left,
                        camera3d_settings.right, camera3d_settings.top,
                        camera3d_settings.top, camera3d_settings.bottom,
                        camera3d_settings.aspect, camera3d_settings.v_fov,
                        camera3d_settings.focal_length, 0, camera3d_settings.camera_width,
                        camera3d_settings.camera_height
                    )
    await p.send_tag('UI_BGCOLOR', *place_class.UISettings.background_color)
    await p.send_tag('P_DRAG', int(place_class.draggable))
    await p.send_tag('P_CAMLIMITS',
                        camera_settings.margin_top_left_x,
                        camera_settings.margin_top_left_y, 
                        camera_settings.margin_bottom_right_x,
                        camera_settings.margin_bottom_right_y
                    )
    await p.send_tag('P_LOCKRENDERSIZE', 0, 1024, 768)
    await p.send_tag('P_LOCKOBJECTS', int(place_class.object_lock))
    await p.send_tag('UI_BGSPRITE', 
                        place_class.UISettings.BackgroundSprite.sprite_id, 
                        place_class.UISettings.BackgroundSprite.fit_type,
                        place_class.UISettings.BackgroundSprite.scale_x,
                        place_class.UISettings.BackgroundSprite.scale_y
                    )
    for i, obj_id in place_class.tile_list:
        tile = get_object(obj_id)
        await p.send_tag('P_TILE', i, tile.url, int(tile.blocking), int(tile.blend), 1, '0:1', 
                         int(tile.tile_mode), int(tile.friction), int(tile.bounce), tile.sprite_id)
    await p.send_tag('P_PHYSICS',
                        int(place_class.Physics.gravity), 
                        int(place_class.Physics.collision),
                        int(place_class.Physics.friction),
                        int(place_class.Physics.tile_friction),
                        int(place_class.Physics.safety_net),
                        place_class.Physics.net_height,
                        int(place_class.Physics.net_friction),
                        int(place_class.Physics.net_bounce)
                    )
    await p.send_tag('P_ASSETSCOMPLETE', 0, 0)