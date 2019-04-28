import bpy
import os

root_path = "\\\\192.168.80.195\data3\LiyouWang"
model_path = os.path.join(root_path, "AlignedHead")
output_path = os.path.join(root_path, "smooth_head")

objs = os.listdir(model_path)
for obj in objs:
    bpy.ops.import_scene.obj(filepath=os.path.join(model_path, obj))
    bpy.context.scene.objects.active=bpy.data.objects[obj[:-4]]
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    bpy.ops.mesh.vertices_smooth(repeat=2)
    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    bpy.ops.export_scene.obj(filepath=os.path.join(output_path, obj), use_selection=True)
    bpy.ops.object.delete()