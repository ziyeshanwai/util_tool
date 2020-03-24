import os
import bpy

"""
remove all the obj in the scene
"""
blendshapes_path = "D:/pycharm_project/FET/transfered/xiaoyue/Charactor/Quad/Head/AlignedBlendshapes"
fbx_output_path = "D:/pycharm_project/FET/transfered/xiaoyue/Charactor/Quad/Head/AlignedBlendshapes"
fbx_name = "{}.fbx".format("xiaoyue")
filenames = os.listdir(blendshapes_path)
base_mesh_name = "base_mesh.obj"
for file in filenames:
    if file.endswith(".obj"):
        bpy.ops.import_scene.obj(filepath=os.path.join(blendshapes_path, file))
        bpy.context.selected_objects[0].name = file[:-4]
for obj in bpy.context.scene.objects:
    obj.select=True
    	
#bpy.data.objects[base_mesh_name[:-4]].select=True
bpy.context.scene.objects.active = bpy.context.selected_objects[-1]
bpy.context.scene.objects.active = bpy.data.objects[base_mesh_name[:-4]]
bpy.ops.object.join_shapes()
bpy.data.objects[base_mesh_name[:-4]].select=False
bpy.ops.object.delete()
bpy.ops.export_scene.fbx(filepath=os.path.join(fbx_output_path, fbx_name), check_existing=True, axis_forward='-Z', axis_up='Y')