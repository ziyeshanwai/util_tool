import bpy
import numpy as np

def creat_object(name, verts, face):
    
    mymesh = bpy.data.meshes.new("Cube")
    myobject = bpy.data.objects.new("Cube", mymesh)
    myobject.name = name
    #Set location and scene of object
    myobject.location = bpy.context.scene.cursor.location
    bpy.context.scene.collection.objects.link(myobject)
    #Create mesh
    mymesh.from_pydata(verts,[],face)
    mymesh.update(calc_edges=True)

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

def get_verts(ob):
    v = get_bone_verts(ob.name)
    v = v.reshape(-1,3).tolist()
    return v

def get_face_list(ob):
    face_list = []
    for i in range(0, len(ob.polygons)):
        face = [v for v in ob.polygons[i].vertices]  # +1 with same with obj file blender start index from 0 not 1
        face_list.append(face)
    return face_list

def print_error(source_ob, target_ob):
    source_verts_np = np.zeros(len(ob_source.data.vertices) * 3, dtype=np.float32)
    ob_source.data.vertices.foreach_get('co', source_verts_np)
    source = source_verts_np.reshape(-1, 3)
    source = np.array(source_ob.matrix_world) @ np.hstack((source, np.ones((source.shape[0],1)))).T
    target_verts = get_bone_verts(target_ob.name)
    target = target_verts.reshape(-1, 3)
    target = np.array(target_ob.matrix_world) @ np.hstack((target, np.ones((target.shape[0],1)))).T
    error = np.mean(np.linalg.norm(source.T[:, :3] - target.T[:, :3], axis=1))
    print("error is {}".format(error))
    return error

def print_error2(source_ob, target_ob):
    source_verts_np = np.zeros(len(ob_source.data.vertices) * 3, dtype=np.float32)
    ob_source.data.vertices.foreach_get('co', source_verts_np)
    source = source_verts_np.reshape(-1, 3)
    source = np.array(source_ob.matrix_world) @ np.hstack((source, np.ones((source.shape[0],1)))).T
    target_np = np.zeros(len(target_ob.data.vertices) * 3, dtype=np.float32)
    target_ob.data.vertices.foreach_get('co', target_np)
    target = target_np.reshape(-1, 3)
    target = np.array(target_ob.matrix_world) @ np.hstack((target, np.ones((target.shape[0],1)))).T
    error = np.mean(np.linalg.norm(source.T[:, :3] - target.T[:, :3], axis=1))
    print("error is {}".format(error))
    return error

if __name__ == "__main__":
    print("--"*100)
    armature = bpy.data.objects["rest_pose"]
    ob_tar = bpy.data.objects["pose_0"]
    ob_source = bpy.data.objects["head_lod0_mesh"]
    face = get_face_list(ob_tar.data)
    v = get_verts(ob_source)
    creat_object("test", v, face)
    print_error2(ob_source, bpy.data.objects["test"])
    target_verts_np = np.zeros(len(ob_tar.data.vertices) * 3, dtype=np.float32)
#    print_error(ob_source, ob_tar)