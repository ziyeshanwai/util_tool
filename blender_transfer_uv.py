import bpy
import os

"""
transfer uvs
"""

uv_exmaples_name = "polySurface1"
model_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\auto_blendshape\\blendshaps_56\\blendshapes"
output_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\auto_blendshape\\blendshaps_56\\uv_blendshape"
filenames = os.listdir(model_path)
for file in filenames:
    if file.endswith(".obj"):
        bpy.ops.import_scene.obj(filepath=os.path.join(model_path, file))
        bpy.data.objects[uv_exmaples_name].select=True
        bpy.context.scene.objects.active=bpy.data.objects[uv_exmaples_name]
        bpy.ops.object.join_uvs()
        bpy.data.objects[uv_exmaples_name].select=False
        bpy.ops.export_scene.obj(filepath=os.path.join(output_path, file), use_selection=True, use_materials=False)
        bpy.ops.object.delete()
    else:
        print("skip {}".format(file))
    