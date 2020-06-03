import bpy
import bmesh
import json
import numpy as np
import os
import pickle

def loadmarkpoint(txt_path):
    with open(txt_path, 'r') as f:
        data = json.load(f)
    mark_points = np.array(data)
    return mark_points

def find_closet_index(points, gt):
    row, col = points.shape
    ind = []
    for i in range(0, row):
        dis = np.sum((gt-points[i])**2, axis=1)
        ind.append(np.argmin(dis))
    return ind

def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))

obj = bpy.context.active_object
bm = bmesh.from_edit_mesh(obj.data)

txtpath = os.path.join(r"\\192.168.20.63\ai\Liyou_wang_data\CTO_2020_03_11\data\basemesh",
                                         "points_233.txt") 

all_co_truth = np.array([vert.co for vert in bm.verts])
point_from_file = loadmarkpoint(txtpath)
ind = find_closet_index(point_from_file, all_co_truth)
print("ind is {}".format(len(ind)))
ind[225] = 6718
ind[216] = 7159
for i in ind:
    print(i)
    bm.verts[i].select_set(True)
save_pickle_file(os.path.join(r"\\192.168.20.63\ai\Liyou_wang_data\cto_2020_06_03\bs_include_eye\base_mesh","obj_ind.pkl"), ind)