import bpy
import mathutils
import numpy as np
import math

def matrix_world(armature_ob, bone_name):
    local = armature_ob.data.bones[bone_name].matrix_local
    basis = armature_ob.pose.bones[bone_name].matrix_basis
    parent = armature_ob.pose.bones[bone_name].parent
    if parent == None:
        return  local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].matrix_local
        return matrix_world(armature_ob, parent.name) @ (parent_local.inverted() @ local) @ basis


def relative_matrix(parent_ob, child_ob):
    """
    calculate the relative matrix c1 is the parent  c2 is the child
    """
    p_w = parent_ob.matrix_world
    c_w = child_ob.matrix_world
    c_p = p_w.inverted() @ c_w
    return c_p

if __name__ == "__main__":
    armature_ob = bpy.data.objects["rest_pose"]
    bone_name = 'neck_02'
    print("world coordinate")
    print(matrix_world(armature_ob, bone_name).translation)
    print(matrix_world(armature_ob, bone_name).to_euler())
    armature_ob.data.bones['neck_02'].matrix_local.translation
    armature_ob.data.bones['neck_02'].matrix_local.to_euler()
    parent_ob = bpy.data.objects['c1']
    child_ob = bpy.data.objects['c2']
    c_w = parent_ob.matrix_world @ child_ob.matrix_local
    translation = c_w.to_translation()
    rotation = c_w.to_euler()
    rotation_degrees = [math.degrees(r) for r in  rotation]
    c_p = relative_matrix(parent_ob, child_ob)
    print("c_p translation is {}".format(c_p.to_translation()))
    print("gt c_p translation is {}".format(child_ob.matrix_local.to_translation()))