import bpy
import os
import mathutils

model_path = "D:\\changeAxis\\Blendshapes"
output_path = "D:\\changeAxis\\New_axis"
obj_names = os.listdir(model_path)

for obj in obj_names:
    bpy.ops.import_scene.obj(filepath=os.path.join(model_path, obj))
    #bpy.types.EXPORT_SCENE_OT_obj.forward="Y"
    #bpy.types.EXPORT_SCENE_OT_obj.axis_up="Z"
    bpy.ops.export_scene.obj(filepath=os.path.join(output_path, obj), use_selection=True, use_materials=False,use_normals=False,axis_forward="Y", axis_up="Z")
    bpy.ops.object.delete()