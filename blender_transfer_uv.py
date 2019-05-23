import bpy
import os

"""
transfer uvs
"""

uv_exmaples_name = "smooth-0"
model_path = "\\\\192.168.80.195\\data3\\LiyouWang\\smoothObjs"
output_path = "\\\\192.168.80.195\\data3\\LiyouWang\\uv_objs"
filenames = os.listdir(model_path)
for file in filenames:
    bpy.ops.import_scene.obj(filepath=os.path.join(model_path, file))
    bpy.data.objects[uv_exmaples_name].select=True
    bpy.context.scene.objects.active=bpy.data.objects[uv_exmaples_name]
    bpy.ops.object.join_uvs()
    py.data.objects[uv_exmaples_name].select=False
	bpy.ops.export_scene.obj(filepath=os.path.join(output_path, file), use_selection=True, use_materials=False)
    bpy.ops.object.delete()
    