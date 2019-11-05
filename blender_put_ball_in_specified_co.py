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
    obj_name = "standard"
    root_path = r"\\192.168.20.63\ai\Liyou_wang_data\blender_add_ball"
    txt_name = "neural-source-points.txt"
    ball_cor_path = os.path.join(root_path, txt_name)
    coordinates = loadmarkpoint(ball_cor_path)
    obj = bpy.data.objects[obj_name]
    for i in range(0, len(coordinates)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, enter_editmode=False, 
        location=obj.matrix_world @ Vector(coordinates[i]))