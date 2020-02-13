import bpy
import bmesh
import pickle
import os
import numpy as np


def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))
co = []
obj=bpy.context.object
if obj.mode == 'EDIT':
    bm=bmesh.from_edit_mesh(obj.data)
    for v in bm.verts:
        if v.select:
            co.append(v.co)
else:
    print("Object is not in edit mode.")

verts = np.empty(len(bpy.context.active_object.data.vertices)*3, dtype=np.float64)   
shape = (len(bpy.context.active_object.data.vertices) ,3)  
# method 1
print("-------------method 1-------------------")
inds = [i.index for i in bpy.context.active_object.data.vertices if i.select]  
co = [i.co for i in bpy.context.active_object.data.vertices if i.select]
bpy.context.active_object.data.vertices.foreach_get('co', verts)  # get
verts.shape = shape
#verts.shape = count*3  
#me.vertices.foreach_set('co', verts)  set

print("numpy verts is {}".format(verts[inds, :]))
contour = verts[inds, :]
tmp_one = np.ones(len(contour))
hmo_contour = np.c_[contour, tmp_one]
contour_world_coor = np.matmul(obj.matrix_world, hmo_contour.T)
contour_world_coor = contour_world_coor.T[:, 0:3]
inds = np.array(inds, dtype=np.int32)[contour_world_coor[:,0].argsort()].tolist()
print("inds is {}".format(inds))
print("co is {}".format(contour_world_coor))



# method 2
print("------------------method2-----------------")
inds = [i.index for i in bmesh.from_edit_mesh(bpy.context.active_object.data).verts if i.select]
print("--------------------")
print(len(inds))
print(inds)
save_pickle_file("./mouth_down_contour.pkl", inds)