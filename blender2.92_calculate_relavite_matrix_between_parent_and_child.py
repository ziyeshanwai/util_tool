import bpy
import mathutils
import numpy as np
import math

"""
blender内计算父子骨骼的相对矩阵
首先使用 matrix_world 计算出父骨骼的世界坐标矩阵 就算出子骨骼的世界坐标矩阵
然后使用 relative_matrix 计算出父子骨骼之间的相对旋转矩阵
"""

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

def test_bone_position():
    """
    get bone head world position
    """

def set_coor(location, rotation):
    """
    visulize result is right or not world_positon world rotation
    """
    rob = bpy.context.scene.objects.get("cor")
    print(rob)
    if not rob:
        bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=location, scale=(1, 1, 1))
        bpy.context.selected_objects[0].name="cor"
    bpy.data.objects["cor"].rotation_euler = rotation
    bpy.data.objects["cor"].location = location
    
def relative_matrix(parent_ob_matrix_world, child_ob_matrix_world):
    """
    calculate the relative matrix c1 is the parent  c2 is the child
    """
    p_w = parent_ob_matrix_world
    c_w = child_ob_matrix_world
    c_p = p_w.inverted() @ c_w
    return c_p

if __name__ == "__main__":
    """
    https://blender.stackexchange.com/questions/44637/how-can-i-manually-calculate-bpy-types-posebone-matrix-using-blenders-python-ap
    matrix_local store the rotation and translation  relative to armature not relative to parent bone !!
    """
    armature_ob = bpy.data.objects["root"]
    armature_ob.pose.bones['b1'].matrix_basis
    euler = armature_ob.data.bones["b1"].matrix_local.to_euler()
    location = armature_ob.data.bones["b1"].matrix_local.to_translation()
    b1_world = armature_ob.data.bones["b0"].matrix_local @ armature_ob.pose.bones["b0"].matrix_basis @ armature_ob.data.bones["b1"].matrix_local @ armature_ob.pose.bones["b1"].matrix_basis
    b1_world = armature_ob.matrix_world @ armature_ob.data.bones["b2"].matrix_local @ armature_ob.pose.bones["b2"].matrix_basis
    euler = b1_world.to_euler()
    location = b1_world.to_translation()
    set_coor(location, euler)
    b1_matrix_world = matrix_world(armature_ob, "b1")
    b0_matrix_wolrd = matrix_world(armature_ob, "b0")
    b1_b0 = relative_matrix(b0_matrix_wolrd, b1_matrix_world) # child relative parent coordinate
    print(b1_b0.to_translation())
    print(b1_b0.to_euler())
    b1_matrix_local = armature_ob.data.bones["b0"].matrix_local @ b1_b0
    print(b1_matrix_local)
    print(armature_ob.data.bones["b1"].matrix_local)
#    euler = b1_world.to_euler()
#    location = b1_world.to_translation()
#    set_coor(location, euler)
#    print([math.degrees(r) for r in euler])
    
    
    
    