"""
ref:https://blender.stackexchange.com/questions/146302/how-to-change-the-location-of-an-addon-in-the-ui
https://blender.stackexchange.com/questions/201367/how-assign-shortcut-to-custom-function
"""
import bpy

bl_info = {
    "name": "Your Addon Name",
    "author": "Liyouwang",
    "version": (0, 1),
    "blender" : (2, 92, 0),
    "location": "",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": ""
}


class OBJECT_OT_CustomOp(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.simple_operator"
    bl_label = "Simple Object Operator"
    
    @classmethod
    def poll(cls, context):
        return  context.space_data.type == 'IMAGE_EDITOR'

    def execute(self, context):
        
        print("im trigered!")
        
        return {'FINISHED'}


addon_keymaps = []

def register():
    bpy.utils.register_class(OBJECT_OT_CustomOp)
    
    # Add the hotkey
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = wm.keyconfigs.addon.keymaps.new(name='Image', space_type='IMAGE_EDITOR') # the name and space_type is fixed, can not custom
        kmi = km.keymap_items.new(OBJECT_OT_CustomOp.bl_idname, type='D', value='PRESS', ctrl=True)
        addon_keymaps.append((km, kmi))


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_CustomOp)
    
    # Remove the hotkey
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()


if __name__ == "__main__":
    register()