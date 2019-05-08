import bpy
import os

root_path = "D:\\blendshapes_Demo\\Blendshape_51"
p1_name = "CurveTemplate_BOD51_BOD_51_c"
parent1 = bpy.data.objects[p1_name]
for child in parent1.children:
    child.select=True
    bpy.ops.export_scene.obj(filepath=os.path.join(root_path, child.name+".obj"), use_selection=True)
    child.select = False