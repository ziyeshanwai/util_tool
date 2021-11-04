import bpy


def worldMatrix(ArmatureObject,Bone):
    _bone = ArmatureObject.pose.bones[Bone]
    _obj = ArmatureObject
    return _obj.matrix_world * _bone.matrix


def worldMatrix2(ArmatureObject,Bone):
    _bone = ArmatureObject.pose.bones[Bone]
    _obj = ArmatureObject
    return _obj.matrix_world @ _bone.bone.matrix_local @ _bone.matrix_basis

def matrix_world(armature_ob, bone_name):
    local = armature_ob.data.bones[bone_name].matrix_local
    basis = armature_ob.pose.bones[bone_name].matrix_basis

    parent = armature_ob.pose.bones[bone_name].parent
    if parent == None:
        return  local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].matrix_local
        return matrix_world(armature_ob, parent.name) @ (parent_local.inverted() @ local) @ basis

def set_bone_basis(armature_ob, bone_name, world_basis):
    """
    set bone to world_basis
    """
    mat = matrix_world(armature_ob, bone_name)
    basis = armature_ob.pose.bones[bone_name].matrix_basis
    H = mat @ basis.inverted()
    _basis = H.inverted() @ armature_ob.matrix_world.inverted() @ world_basis
    armature_ob.pose.bones[bone_name].matrix_basis.translation = _basis.translation
    return None


empty_ob = bpy.data.objects["Cube"]
armature_ob = bpy.data.objects["rest_pose"]
world_basis = empty_ob.matrix_basis
#bone_name = bpy.context.active_pose_bone.name
bone_name = "neck_02"
set_bone_basis(armature_ob, bone_name, world_basis)

print(matrix_world(armature_ob, bone_name))
print(worldMatrix2(armature_ob,bone_name))
#empty_ob.matrix_world = armature_ob.matrix_world @ matrix_world(armature_ob, bone_name)
#empty_ob.matrix_world = worldMatrix(armature_ob, bone_name )