"""
a demo for short key add property and delete property
https://blender.stackexchange.com/questions/201367/how-assign-shortcut-to-custom-function
"""
import bpy

bl_info = {
    "name": "TestAddAndDeleteProperty",
    "author": "Liyou Wang",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "location": "View3D > Select > AddProperty",
    "description": "TestAddAndDeleteProperty",
    "warning": "",
    "wiki_url": "",
    "category": "3D View",
}

class AddProperty(bpy.types.Operator):
    """add acticve object property"""
    bl_idname = "object.add_property"
    bl_label = "add_property"
    bl_description = "add_property"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    def invoke(self, context, event):
        bpy.context.active_object["binary_coordinate"] = {"faceid":1, "w1":0.5, "w2":0.5}
        return {'PASS_THROUGH'}
    
class DeleteProperty(bpy.types.Operator):
    """delete acticve object property"""
    bl_idname = "object.delete_property"
    bl_label = "delete_property"
    bl_description = "delete_property"
    bl_space_type = "VIEW_3D"
    bl_region_type = 'UI'

    @classmethod
    def poll(cls, context):
        return context.space_data.type == 'VIEW_3D'

    def invoke(self, context, event):
        del bpy.context.active_object["binary_coordinate"]
        return {'PASS_THROUGH'}

def menu_func(self, context): ## creating the menu item
    self.layout.operator(AddProperty.bl_idname, icon='MESH_CUBE')
    self.layout.operator(DeleteProperty.bl_idname, icon='MESH_CUBE') 
       
classess = [AddProperty, DeleteProperty]

def register():
    for cls in classess:
        bpy.utils.register_class(cls)
    bpy.types.VIEW3D_MT_select_object.append(menu_func)
        


#    wm = bpy.context.window_manager
#    kc = wm.keyconfigs['Blender User']
#    km = kc.keymaps['3D View']
#    kmi = km.keymap_items.new(ViewOperatorRayCast.bl_idname, 'MOUSEMOVE', 'ANY', ctrl=True)


def unregister():
    for cls in classess:
        bpy.utils.unregister_class(cls)
        
    bpy.types.VIEW3D_MT_select_object.remove(menu_func)

        
if __name__ == "__main__":
    register()