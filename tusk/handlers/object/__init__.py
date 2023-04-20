from tusk.handlers import slash_command


@slash_command('anim_done')
async def object_animation_done(p, obj_id, handle_id):
    object = p.objects.get_object(int(obj_id))
    if object is None:
        return
    callback = object.callbacks.get(int(handle_id))
    if callback is not None:
        await callback(p)