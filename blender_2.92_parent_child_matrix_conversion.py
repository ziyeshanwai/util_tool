import bpy
import mathutils
import numpy as np
import math

def matrix_world(armature_ob, bone_name):
    """
    get the specifid bone world matrix
    """
    local = armature_ob.data.bones[bone_name].matrix_local
    basis = armature_ob.pose.bones[bone_name].matrix_basis
    parent = armature_ob.pose.bones[bone_name].parent
    if parent == None:
        return  local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].matrix_local
        return matrix_world(armature_ob, parent.name) @ (parent_local.inverted() @ local) @ basis
    
def relative_matrix(parent_ob_matrix_world, child_ob_matrix_world):
    """
    calculate the relative matrix c1 is the parent  c2 is the child
    """
    p_w = parent_ob_matrix_world
    c_w = child_ob_matrix_world
    c_p = p_w.inverted() @ c_w
    return c_p

if __name__ == "__main__":
    armature_ob = bpy.data.objects["rest_pose"]
    parent_bone_name = 'FACIAL_C_FacialRoot'
    child_bone_name = "FACIAL_L_ForeheadMid"
    parent_matrix_world = matrix_world(armature_ob, parent_bone_name)
    child_matrix_world = matrix_world(armature_ob, child_bone_name)
    relative_matrix = relative_matrix(parent_matrix_world, child_matrix_world)
    print(relative_matrix.to_translation())
    print([math.degrees(r) for r in relative_matrix.to_euler()])