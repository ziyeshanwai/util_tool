import bpy
import os
import pickle
from mathutils import Vector


def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))
        

if __name__ == "__main__":
    points_path = r"\\192.168.20.63\ai\double_camera_data\2020-05-28\155026\output_with_eye_1\debug\3d_points"
    points = load_pickle_file(os.path.join(points_path, "{}.pkl".format(0)))
    for i in range(0, len(points)):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, enter_editmode=False, align='WORLD', location=(0,0,0))
        bpy.context.selected_objects[0].name = str(i)
        
    for i in range(0, 666):
        points = load_pickle_file(os.path.join(points_path, "{}.pkl".format(i)))
       # print(points.shape)
        for j in range(0, len(points)):
            bpy.data.objects[str(j)].location = bpy.data.objects[str(j)].matrix_world @ Vector(points[j, :])
            bpy.data.objects[str(j)].keyframe_insert(data_path="location",frame=i)
            
       # bpy.context.scene.tool_settings.use_keyframe_insert_auto = True
