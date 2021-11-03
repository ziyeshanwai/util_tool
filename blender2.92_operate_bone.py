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

def armature_offset2pose_offset():
    mat_local_to_parent = (
    bone.matrix_local if bone.parent is None else
    bone.parent.matrix_local.inverted() * bone.matrix_local)
    pos = mat_local_to_parent.to_translation()
    quat = mat_local_to_parent.to_quaternion().inverted()
    return 

def armature_position2pose_position(bone, position):
    pose_position = bone.matrix_local.inverted() @ position
    return pose_position


def matrix_world(armature_ob, bone_name):
    """
    https://blender.stackexchange.com/questions/44637/how-can-i-manually-calculate-bpy-types-posebone-matrix-using-blenders-python-ap
    """
    local = armature_ob.data.bones[bone_name].bone.matrix_local
    basis = armature_ob.pose.bones[bone_name].matrix_basis

    parent = armature_ob.pose.bones[bone_name].parent
    if parent == None:
        return  local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].bone.matrix_local
        return matrix_world(armature_ob, parent.name) @ (parent_local.inverted() @ local) @ basis
bons_list[3].bone.matrix_local @ bons_list[3].matrix_basis @ (bons_list[3].bone.matrix_local.inverted() @ bones_list[4].bone.matirx_local) @ bones_list[4].matrix_basis
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