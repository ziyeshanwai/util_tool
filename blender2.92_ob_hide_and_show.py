import os
import bpy
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
    num_points = 108
    points_path = r""
    # bpy.data.objects["root"].parent = None
    matrix_world_ob = bpy.data.objects["head_geo"]
    bpy.ops.object.empty_add(type='PLAIN_AXES', align='WORLD', location=(0, 0, 0), scale=(1, 1, 1))
    bpy.context.selected_objects[0].name = "ROOT"
    for i in range(0, num_points):
            bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, enter_editmode=False, align='WORLD', location=(0,0,0))
            bpy.context.selected_objects[0].name = str(i)
            bpy.context.selected_objects[0].parent = bpy.data.objects["ROOT"]
    points_name_list = os.listdir(points_path)
    for i, name in enumerate(points_name_list):
        points = load_pickle_file(os.path.join(points_path, name))
        ind = []
        frame_num = int(name[:-4])
        if i % 100 == 0:
            print("process {}".format(i))
        for point in points:
            bpy.data.objects[str(point[0])].location = matrix_world_ob.matrix_world @ Vector(point[1])
            bpy.data.objects[str(point[0])].keyframe_insert(data_path="location",frame=frame_num)
            bpy.data.objects[str(point[0])].hide_viewport = False
            bpy.data.objects[str(point[0])].keyframe_insert(data_path='hide_viewport', frame=frame_num)
            ind.append(point[0])
            
        for j in range(0, num_points):
            if j in ind:
                pass
            else:
                bpy.data.objects[str(j)].hide_viewport = True
                bpy.data.objects[str(j)].keyframe_insert(data_path='hide_viewport', frame=frame_num)