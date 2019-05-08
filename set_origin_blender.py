import bpy
import os
import mathutils

model_path = "D:\\blendshapes_Demo\\Blendshape_51"
output_path = "D:\\blendshapes_Demo\\Blendshape_51_align"
obj_names = os.listdir(model_path)

for obj in obj_names:
    bpy.ops.import_scene.obj(filepath=os.path.join(model_path, obj))
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')
    bpy.context.selected_objects[0].location = mathutils.Vector((0,0,0))
    bpy.ops.export_scene.obj(filepath=os.path.join(output_path, obj), use_selection=True, use_materials=False)
    bpy.ops.object.delete()