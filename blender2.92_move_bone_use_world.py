import bpy
import mathutils
import numpy as np

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
    set bone to world_basis translation not change rotation
    """
    mat = matrix_world(armature_ob, bone_name)
    basis = armature_ob.pose.bones[bone_name].matrix_basis
    H = mat @ basis.inverted()
    _basis = H.inverted() @ armature_ob.matrix_world.inverted() @ world_basis
    armature_ob.pose.bones[bone_name].matrix_basis.translation = _basis.translation
    return None

def build_kdtree(ob):
    mesh = ob.data
    size = len(mesh.vertices)
    kd = mathutils.kdtree.KDTree(size)
    for i, v in enumerate(mesh.vertices):
        kd.insert(v.co, i)
    kd.balance()
    return kd

def kdtree_search(kd, co_find):
    co, index, dist = kd.find(co_find)
    return co, index, dist

def check_vertice_in_vertex_group(ob_source, index, vertex_group_name):
    vertice = ob_source.data.vertices[index]
    gp_index = [g.group for g in vertice.groups]
    true_group_index = ob_source.vertex_groups[vertex_group_name].index
    if true_group_index in gp_index: # if nn points is not in 
        return True
    else:
        return False


if __name__ == "__main__":
    
    armature = bpy.data.objects["rest_pose"]
    ob_tar = bpy.data.objects["target_bs"]
    ob_source = bpy.data.objects["mesh"]
    source_verts_np = np.zeros(len(ob_source.data.vertices) * 3, dtype=np.float32)
    target_verts_np = np.zeros(len(ob_tar.data.vertices) * 3, dtype=np.float32)
    ob_source.data.vertices.foreach_get('co', source_verts_np)
    ob_tar.data.vertices.foreach_get('co', target_verts_np)
    bones_list = armature.pose.bones # pose mode using 
    edit_bones_list = armature.data.edit_bones # edit mode using
    kd_tree = build_kdtree(ob_source)
    print("--"*(100))
    num_bones = 0
    for bone in bones_list:
        bone_position = bone.head     
#        np_dist = np.array((bone_position1 - bone_position2).to_tuple())
        
        _, index, dist = kdtree_search(kd_tree, bone_position)
        if ob_source.vertex_groups.find(bone.name) != -1: ## exist the vertex group
            if not check_vertice_in_vertex_group(ob_source, index, bone.name):
               print("find new nearest points")
               for (co, ind, dist) in kd_tree.find_n(bone_position, 100): ## choose top 100
                    if check_vertice_in_vertex_group(ob_source, ind, bone.name):
                        index = ind
                        break
                

        if bone.name == "":
            print(check_vertice_in_vertex_group(ob_source, index, bone.name))
            print("index:{}, dist:{}".format(index, dist))
        if dist < 1000:
            offset = ob_source.data.vertices[index].co - bone_position # should keep
            bones_position_new = ob_tar.matrix_world @ ob_tar.data.vertices[index].co - ob_source.matrix_world @ offset
            bones_new_basis = ob_tar.matrix_basis.copy()
            bones_new_basis.translation = bones_position_new
            set_bone_basis(armature, bone.name, bones_new_basis)
        
            if ob_source.vertex_groups.find(bone.name)==-1: # exist in vertexs group 1: exist -1: not exist
#                print("{}:{}:{}".format(bone.name, index, dist))
                num_bones +=1
#    print("vertex group:{}".format(len(ob_source.vertex_groups)))
#    print("{} bones has no weight".format(len(bones_list) - len(ob_source.vertex_groups)))
#    print("dist great 5e-5:{}".format(num_bones))