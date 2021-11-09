import bpy
import numpy as np
import scipy.optimize as optimize


def get_bone_verts(ob_name):
    obj = bpy.data.objects[ob_name]
    count = len(obj.data.vertices)
    verts = np.zeros(count*3, dtype=np.float32)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = obj.evaluated_get(depsgraph)
    mesh_from_eval = object_eval.to_mesh()
    b = mesh_from_eval.vertices.foreach_get("co", verts)
    object_eval.to_mesh_clear()
    b = verts
    return b

def error(source_ob, target_ob):
    source_verts_np = np.zeros(len(source_ob.data.vertices) * 3, dtype=np.float32)
    source_ob.data.vertices.foreach_get('co', source_verts_np)
    source = source_verts_np.reshape(-1, 3)
    source = np.array(source_ob.matrix_world) @ np.hstack((source, np.ones((source.shape[0],1)))).T
    target_verts = get_bone_verts(target_ob.name)
    target = target_verts.reshape(-1, 3)
    target = np.array(target_ob.matrix_world) @ np.hstack((target, np.ones((target.shape[0],1)))).T
    error_array = np.linalg.norm(source.T[:, :3] - target.T[:, :3], axis=1)
    error = np.mean(np.linalg.norm(source.T[:, :3] - target.T[:, :3], axis=1))
    print("error is {}".format(error))
    return error_array

def get_joint_group(ob, ind):
    bone_index = [g.group for i in ind for g in ob.data.vertices[i].groups] 
    bone_index = set(bone_index)
    bone_name = [ob.vertex_groups[ind].name for ind in bone_index]
    print("there is {} bone".format(len(bone_name)))
    print(bone_name)
    return bone_name
    
def func_trans_loss(x, armature, bone_names, ind, source_ob, target_ob_vertice_array):
    """
    target_ob_vertice_array: n , 3
    """
    # assign valut to bone_name 
    tmp = x.reshape(-1, 3)
#    print("tmp is {}".format(tmp))
    for i, bone_name in enumerate(bone_names):
        armature.pose.bones[bone_name].location.x = tmp[i, 0]
        armature.pose.bones[bone_name].location.y = tmp[i, 1]
        armature.pose.bones[bone_name].location.z = tmp[i, 2]
    v = get_bone_verts(source_ob.name) # update vertex positon
    v_n = v.reshape(-1, 3)
    r = np.array(ob_source.matrix_world) @ np.hstack((v_n, np.ones((v_n.shape[0],1)))).T
    v = r.T[:, :3] # convert to world coordinate
    # calculate the error 
    loss = np.mean(np.linalg.norm(v[ind, :] - target_ob_vertice_array[ind, :], axis=1))
    return loss

def func_rotation_loss(x, armature, bone_names, ind, source_ob, target_ob_vertice_array):
    """
    target_ob_vertice_array: n , 3
    """
    # assign valut to bone_name 
    tmp = x.reshape(-1, 3)
#    print("tmp is {}".format(tmp))
    for i, bone_name in enumerate(bone_names):
        armature.pose.bones[bone_name].rotation_euler.x = tmp[i, 0]
        armature.pose.bones[bone_name].rotation_euler.y = tmp[i, 1]
        armature.pose.bones[bone_name].rotation_euler.z = tmp[i, 2]
    v = get_bone_verts(source_ob.name) # update vertex positon
    v_n = v.reshape(-1, 3)
    r = np.array(ob_source.matrix_world) @ np.hstack((v_n, np.ones((v_n.shape[0],1)))).T
    v = r.T[:, :3] # convert to world coordinate
    # calculate the error 
    loss = np.mean(np.linalg.norm(v[ind, :] - target_ob_vertice_array[ind, :], axis=1))
    return loss


def convert2world(ob):
    ob_np = np.zeros(len(ob.data.vertices) * 3, dtype=np.float32)
    ob.data.vertices.foreach_get('co', ob_np)
    ob_np = ob_np.reshape(-1, 3)
    r = np.array(ob.matrix_world) @ np.hstack((ob_np, np.ones((ob_np.shape[0],1)))).T
    return r.T[:, :3]

 
if __name__ == "__main__":
    print("--"*(100))
    armature = bpy.data.objects["rest_pose"]
    ob_tar = bpy.data.objects["pose_0"]
    ob_source = bpy.data.objects["head_lod0_mesh"]
#    target_verts_np = np.zeros(len(ob_tar.data.vertices) * 3, dtype=np.float32)
#    error = print_error(ob_tar, ob_source)
#    show_ob_error(ob_source, error)
#    ob_tar.data.vertices.foreach_get('co', target_verts_np)
#    target_verts_np = target_verts_np.reshape(-1, 3)
    target_verts_np = convert2world(ob_tar)
    error_array = error(ob_tar, ob_source)
    cut_off_error = 0.5
    max_error_ind = np.where(error_array>cut_off_error)[0]
    bone_names = get_joint_group(ob_source, max_error_ind)
    v = get_bone_verts(ob_source.name) # update vertex positon
    v_n = v.reshape(-1, 3)
    r = np.array(ob_source.matrix_world) @ np.hstack((v_n, np.ones((v_n.shape[0],1)))).T
    v = r.T[:, :3]
    print("mean error is {}".format(np.mean(error_array[max_error_ind])))
    error = np.mean(np.linalg.norm(v[max_error_ind, :] - target_verts_np[max_error_ind, :], axis=1))
    print("before optimization error is {}".format(error))
    xt0 = []
    for bone_name in bone_names:
        xt0.append(armature.pose.bones[bone_name].location.x)
        xt0.append(armature.pose.bones[bone_name].location.y)
        xt0.append(armature.pose.bones[bone_name].location.z)
    xr0 = []
    for bone_name in bone_names:
        armature.pose.bones[bone_name].rotation_mode = "XYZ"
        xr0.append(armature.pose.bones[bone_name].location.x)
        xr0.append(armature.pose.bones[bone_name].location.y)
        xr0.append(armature.pose.bones[bone_name].location.z)
    res = optimize.least_squares(func_trans_loss, xt0, ftol=1e-8, xtol=1e-8, gtol=1e-8, max_nfev=200, verbose=1, args=(armature, bone_names, max_error_ind, ob_source, target_verts_np))
#    res = optimize.least_squares(func_rotation_loss, xr0, ftol=1e-8, xtol=1e-8, gtol=1e-8, max_nfev=200, verbose=1, args=(armature, bone_names, max_error_ind, ob_source, target_verts_np))
    print("after optimization loss is {}".format(res.fun))
    v = get_bone_verts(ob_source.name) # update vertex positon
    v_n = v.reshape(-1, 3)
    r = np.array(ob_source.matrix_world) @ np.hstack((v_n, np.ones((v_n.shape[0],1)))).T
    v = r.T[:, :3]
    error = np.mean(np.linalg.norm(v[max_error_ind, :] - target_verts_np[max_error_ind, :], axis=1))
    print("after optimization error is {}".format(error))