import bpy
import os
import json
import numpy as np
from mathutils import Vector

def loadmarkpoint(txt_path):
    with open(txt_path, 'r') as f:
        data = json.load(f)
    mark_points = np.array(data)
    return mark_points


if __name__ == "__main__":
    obj_name = "Head_baseTopo_01"
    root_path = r"\\192.168.20.63\ai\mask\20200226"
    txt_name = "208_xyz.txt"
    ball_cor_path = os.path.join(root_path, txt_name)
    coordinates = loadmarkpoint(ball_cor_path)
    obj = bpy.data.objects[obj_name]
    for i in range(0, len(coordinates)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, enter_editmode=False, 
        location=obj.matrix_world @ Vector(coordinates[i]))
        ao = bpy.context.active_object
        ao.name = "{}".format(i)
    
    solidify = obj.modifiers.new(name="solidify", type="SOLIDIFY")
    solidify.thickness = 0.05
    bpy.ops.object.modifier_apply({"object": obj},apply_as='DATA',modifier=solidify.name)

    for i in range(0, len(coordinates)):
        bool = obj.modifiers.new(name='booly', type='BOOLEAN')
        bool.object = bpy.data.objects["{}".format(i)]
        bool.operation = 'DIFFERENCE'
        bpy.ops.object.modifier_apply({"object": obj},apply_as='DATA',modifier=bool.name)
        bpy.data.objects["{}".format(i)].hide_set(True)
		bpy.data.objects["{}".format(i)].select_set(True)
		bpy.ops.object.delete()
        