import bpy
import os

root_path = "\\\\192.168.80.195\\data3\\LiyouWang"
model_path = os.path.join(root_path, "dist_0419")
output_path = os.path.join(root_path, "Join_dist_0419")

objs = os.listdir(model_path)
for obj in objs:
    bpy.ops.import_scene.obj(filepath=os.path.join(model_path, obj))
    bpy.ops.object.select_all(action="DESELECT")
    bpy.context.scene.objects[0].select=True
    bpy.context.scene.objects[1].select=True
    bpy.context.scene.objects.active = bpy.context.scene.objects[1]
    bpy.ops.object.join()

    bpy.context.scene.objects[0].select=True
    bpy.context.scene.objects[1].select=True
    bpy.context.scene.objects.active = bpy.context.scene.objects[1]
    bpy.ops.object.join()

    bpy.context.scene.objects[0].select=True
    bpy.context.scene.objects[1].select=True
    bpy.context.scene.objects.active = bpy.context.scene.objects[1]
    bpy.ops.object.join()

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.remove_doubles() # remove double_points
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False) # 
    bpy.ops.export_scene.obj(filepath=os.path.join(output_path, obj), use_selection=True)
    bpy.ops.object.delete()