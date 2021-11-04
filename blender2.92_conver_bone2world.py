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
    if parent is not None:
        print("parent name is {}".format(parent.name))
    if parent == None:
        return  local @ basis
    else:
        parent_local = armature_ob.data.bones[parent.name].matrix_local
        return matrix_world(armature_ob, parent.name) @ parent_local.inverted() @ local @ basis

empty_ob = bpy.data.objects["Cube"]
armature_ob = bpy.data.objects["rest_pose"]

#bone_name = bpy.context.active_pose_bone.name
bone_name = "head"
print(matrix_world(armature_ob, bone_name))
print(worldMatrix2(armature_ob, bone_name))
empty_ob.matrix_world = armature_ob.matrix_world @ matrix_world(armature_ob, bone_name)
#empty_ob.matrix_world = worldMatrix(armature_ob, bone_name )