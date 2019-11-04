import os
import bpy

"""
remove all the obj in the scene
"""
blendshapes_path = r"\\192.168.20.63\ai\Liyou_wang_data\faceGood\facegood_s"
fbx_output_path = r"\\192.168.20.63\ai\Liyou_wang_data\faceGood\morph"
fbx_name = "{}.fbx".format("xiaoyue")
filenames = os.listdir(blendshapes_path)
base_mesh_name = "head_geo.obj"
for file in filenames:
    if file.endswith(".obj"):
        bpy.ops.import_scene.obj(filepath=os.path.join(blendshapes_path, file))
for obj in bpy.context.scene.objects:
    obj.select_set(True)
        
#bpy.data.objects[base_mesh_name[:-4]].select=True
bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
bpy.context.view_layer.objects.active = bpy.data.objects[base_mesh_name[:-4]]
bpy.ops.object.join_shapes()
bpy.data.objects[base_mesh_name[:-4]].select_set(False)
bpy.ops.object.delete()
bpy.ops.export_scene.fbx(filepath=os.path.join(fbx_output_path, fbx_name), check_existing=True, axis_forward='-Z', axis_up='Y')