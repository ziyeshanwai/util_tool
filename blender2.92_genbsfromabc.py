import bpy
import bmesh
import numpy as np
from sklearn.decomposition import PCA


def get_frame_verts(ob_name):
    """
    get vertex data
    """
    obj = bpy.data.objects[ob_name]
    count = len(obj.data.vertices)
    verts = np.zeros(count*3, dtype=np.float32)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = obj.evaluated_get(depsgraph)
    mesh_from_eval = object_eval.to_mesh()
    b = mesh_from_eval.vertices.foreach_get("co", verts)
    #mesh_from_eval = bpy.data.meshes.new_from_object(object_eval)  # debug
    object_eval.to_mesh_clear()
    b = verts
    return b

def read_vertex_data_range(ob_name):
    """
    read vertex data between start and end frame the input should be abc file not mesh sequence
    """
    ob = bpy.data.objects[ob_name]
    vert_frame_0 = None
    verts_array = None
    for frame_num in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
        vert = get_frame_verts(ob_name)
        vert = vert.reshape(-1, 1)
        if frame_num == bpy.context.scene.frame_start:
            vert_frame_0 = vert
            verts_array = vert
        else:
            verts_array = np.hstack((verts_array, vert))
        if frame_num % 100 == 0:
            print("read frame {} data".format(frame_num))
        bpy.context.scene.frame_current += 1
    return vert_frame_0, verts_array

def build_pca_commponents(vert_frame_0, verts_array):
    """
    build pca commponent
    """
    n_components_number = 0.9999
    verts_row_samples = verts_array.transpose()
    mean_value = vert_frame_0.reshape(-1,)
    verts_row_samples_mean = verts_row_samples - mean_value
    pca = PCA(n_components=n_components_number, whiten=False)
    pca.fit(verts_row_samples_mean)
    data_reduced = pca.transform(verts_row_samples_mean)
    print("coe shape  is {}".format(data_reduced.shape))
    print("feature vector shape is {}".format(pca.components_.shape))
    print("explained rate is {}".format(np.sum(pca.explained_variance_ratio_)))
    feature_commponents = np.zeros(pca.components_.shape, dtype=np.float32)
    for i in range(0, pca.components_.shape[0]):
        coe = data_reduced[:, i]
        max_value = np.max(np.abs(coe))
        if max_value > 1:
            n = max_value / 1
        else:
            n = 1
        feature_vector = pca.components_[i, :] * n + mean_value
        feature_commponents[i, :] = feature_vector
        data_reduced[:, i] = coe / n
    ones = np.ones((data_reduced.shape[0], 1), dtype=np.float32) 
    bs_coe = np.hstack((data_reduced, ones))   
    corrective = mean_value + pca.mean_ # coe is one
    mean_value = corrective[np.newaxis, :]
    feature_commponents = np.vstack((feature_commponents, mean_value))
    print("bs_coe shape is {}".format(bs_coe.shape))
    return feature_commponents, bs_coe, vert_frame_0

def add_shapekey(ob, shapkeyname, verts_np):
    """
    add shapekey for ob use shapkeyname and verts_np
    """
    if ob.data.shape_keys: ## exist shapkey
        tmp = ob.shape_key_add()
        tmp.name = shapkeyname
    else:
        tmp = ob.shape_key_add()
        tmp.name = "Basis"
        tmp = ob.shape_key_add()
        tmp.name = shapkeyname
    tmp.data.foreach_set('co', verts_np)
    tmp.data.update()
    
def generate_newobject(name, from_ob):
    """
    using bmesh generate new object, then use numpy foreach_set set vertice position
    """
    bm = bmesh.new()
    bm.from_mesh(from_ob.data)
    emptyMesh = bpy.data.meshes.new(name)
    theObj = bpy.data.objects.new(name, emptyMesh)
    bpy.context.scene.collection.objects.link(theObj)
    bm.to_mesh(emptyMesh)
    bm.free()
    theObj.rotation_euler = from_ob.rotation_euler
    return theObj

def set_ob_vertice(ob, verts_np):
    """
    set obj vertex
    """
    
    ob.data.vertices.foreach_set('co', verts_np)
    ob.data.update()

def get_current_ob_vertice(ob):
    """
    get current ob vertices 
    """
    count = len(ob.data.vertices)
    verts = np.zeros(count*3, dtype=np.float32)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = ob.evaluated_get(depsgraph)
    mesh_from_eval = object_eval.to_mesh()
    b = mesh_from_eval.vertices.foreach_get("co", verts)
    object_eval.to_mesh_clear()
    return verts

def build_shapekeys():
    ob_name = "ProjectShan_sequence.001"
    vert_mean, verts_array = read_vertex_data_range(ob_name)
    print("start calculate pca")
    feature_commponents, bs_coe, vert_frame_0 = build_pca_commponents(vert_mean, verts_array)
    pca_ob = generate_newobject("pca_ob", bpy.data.objects[ob_name])
    set_ob_vertice(pca_ob, vert_frame_0)
    print("pca finish!")
    for i, vec in enumerate(feature_commponents):
        add_shapekey(pca_ob, "pcac{}".format(i),vec)
    i = 0
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    for frame_num in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):    
        
        for j, block in enumerate(pca_ob.data.shape_keys.key_blocks):
            if block.name != "Basis":
                block.value=bs_coe[i, j-1]
                block.keyframe_insert("value", frame=frame_num)
        if frame_num % 50 == 0:
            print("insert {}".format(frame_num))
        bpy.context.scene.frame_current += 1  
        i += 1  

if __name__ == "__main__":
#    ob_name = "ProjectShan_sequence.001"
#    vert_mean, verts_array = read_vertex_data_range(ob_name)
#    feature_commponents, bs_coe, vert_frame_0 = build_pca_commponents(vert_mean, verts_array)
     build_shapekeys()   