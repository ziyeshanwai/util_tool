import numpy as np
import bpy
import os
from scipy.optimize import nnls


class FitWeights:
    """
    fit weights
    """

    def __init__(self, A, mean_vert, regu_lar=False, lamb=1.0):
        """
        A 为blendshape 系数
        :param A:
        """
        self.A = A.T
        self.weight = None
        self.regular = regu_lar
        # self.mean_verts = mean_verts
        if self.regular:
            self.lamb = lamb
            self.n_variables = self.A.shape[1]
            self.A2 = np.concatenate([self.A, np.sqrt(self.lamb) * np.eye(self.n_variables)])

    def fit(self, b):
        """
        拟合权重
        :param b:
        :return:
        """
        if self.regular:
            b = np.concatenate([b, np.zeros(self.n_variables)])
            self.weight, error = nnls(self.A2, b)
        else:
            self.weight, error = nnls(self.A, b)
        print("nnls error is {}".format(error))
        return self.weight

    def recover_obj(self):
        obj_vert = self.A.dot(self.weight) + mean_verts
        return obj_vert


def build_A(ob_name):
    ob = bpy.data.objects[ob_name]
    verts = []
    mean = None
    count = len(ob.data.shape_keys.key_blocks[0].data)
    for block in ob.data.shape_keys.key_blocks:
        verts_np = np.zeros(count * 3, dtype=np.float32)
        if block.name == "Basis":
            block.data.foreach_get('co', verts_np)
            mean = verts_np
        else:
            block.data.foreach_get('co', verts_np)
            verts.append(verts_np.tolist())
    A = np.array(verts) - mean
    return A, mean
    
def get_shapekey_names(ob_name):
    """
    get shapekey names
    """
    obj = bpy.data.objects[ob_name]
    shape_key_names = [block.name for block in obj.data.shape_keys.key_blocks]
    return shape_key_names

def get_shapekeys_co(ob_name):
    """
    get shape key local co
    """
    obj = bpy.data.objects[ob_name]
    
    
def get_animation_verts(ob_name):
    """
    get the b in ax = b
    """
    "metahuman_004_FaceMesh"
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

def set_obj_vertice(ob_name, vertice_data):
    """
    set animaiton data
    """
    obj = bpy.data.objects[ob_name]
    #obj.mat
    #depsgraph = bpy.context.evaluated_depsgraph_get()
    #object_eval = obj.evaluated_get(depsgraph)
    
    obj.data.vertices.foreach_set("co", vertice_data)
    obj.data.update()
    bpy.context.view_layer.update()  # update display data
    
def fit_weights(animation_name, ob_name):
    A, mean_verts = build_A(ob_name)
    fit_solver = FitWeights(A, mean_verts, True, 1.0)
    obj = bpy.data.objects[ob_name]
    print("obj_name is {}".format(obj.name))
    bpy.context.scene.frame_current = bpy.context.scene.frame_start
    for frame_num in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
        b = get_animation_verts(animation_name)
        weight = fit_solver.fit(b-mean_verts)
        for i, block in enumerate(obj.data.shape_keys.key_blocks):
            if block.name != "Basis":
                block.value=weight[i-1]
                block.keyframe_insert("value", frame=frame_num)
        print("insert {}".format(frame_num))
        bpy.context.scene.frame_current += 1
    #return weight
    

if __name__ == "__main__":
    ob = "head_geo"
    names = get_shapekey_names(ob)
    print("len of name is {}".format(len(names)))
   # A, mean_verts = build_A(ob)
   # fit_solver = FitWeights(A, mean_verts, True, 30.0)
   # print(names)
    animation_name = "debug_mesh"
    b = get_animation_verts(animation_name)
    #debug_name = "debug"
    #set_obj_vertice(debug_name, b)
    fit_weights(animation_name, ob)
   