import bpy
import numpy as np
import mathutils


def pose_coordinate2armature_coor():
    """
    equals bones_list[0].head
    convert bone pose mode coordinate to armature edit mode coordinate unit:cm
    example code
    """
    return bones_list[0].bone.matrix_local @ bones_list[0].location
def armature_coor2world_coor():
    """
    convert armature edit mode coordinate to world coordinate 
    example code
    """
    return armature.matrix_world @ bones_list[0].head

def build_kdtree(ob):
    mesh = ob.data
    size = len(mesh.vertices)
    kd = mathutils.kdtree.KDTree(size)
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
    kd.balance()
    return kd

def kdtree_search(kd, co_find):
    
    co_find = (0.0, 0.0, 0.0)
    co, index, dist = kd.find(co_find)
    print("Close to center:", co, index, dist)
    co_find = obj.matrix_world.inverted() @ context.scene.cursor.location
    print("Close 10 points")
    for (co, index, dist) in kd.find_n(co_find, 10):
        print("    ", co, index, dist)
    print("Close points within 0.5 distance")
    for (co, index, dist) in kd.find_range(co_find, 0.5):
        print("    ", co, index, dist)
    return co, index, dist
    
"""
if the armature origin is the same with vertices origin,and their coordinate towards is the same
the they are in the same coordinate space
"""
armature = bpy.data.objects["rest_pose"]
ob_tar = bpy.data.objects["target_bs"]
ob_source = bpy.data.objects["mesh"]
source_verts_np = np.zeros(len(ob_source.data.vertices) * 3, dtype=np.float32)
target_verts_np = np.zeros(len(ob_tar.data.vertices) * 3, dtype=np.float32)
ob_source.data.vertices.foreach_get('co', source_verts_np)
ob_tar.data.vertices.foreach_get('co', target_verts_np)
bones_list = armature.pose.bones # pose mode using 
offset = mathutils.Vector([100, 100, 100])
bones_list[0].location += bones_list[0].bone.matrix_local.inverted() @ offset
edit_bones_list = armature.data.edit_bones # edit mode using
for bone in bones_list:
    print("name:{}".format(bone.name))
    print("co:{}".format(bone.head))