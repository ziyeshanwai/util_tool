import bpy
import bmesh
import os
import pickle

"""
auto choose start and end points
"""
def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))
        
def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))

def choose_vertex(file_path):
    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    verts_index = [v.index for v in bm.verts if v.select]
    print("verts_index is {}".format(verts_index))
    save_pickle_file(os.path.join(file_path, "tmp.pkl"), verts_index)

def select_verts(file_path):
    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    verts_index = load_pickle_file(os.path.join(file_path, "tmp.pkl"))
    print("verts_index is {}".format(verts_index))
    for i in verts_index:
         bm.verts[i].select_set(True)
    bmesh.update_edit_mesh(me, True) 

def generate_contour(file_path, name):        
    contour_path = file_path
    file_name = "{}.pkl".format(name)
    ob = bpy.context.object
    me = ob.data
    bm = bmesh.from_edit_mesh(me)
    verts = [v for v in bm.verts if v.select]
    verts_world = [ob.matrix_world @ v.co for v in verts]
    index = [i for i in range(0, len(verts_world))]
    zip_ind_verts = zip(index, verts_world)
    verts_world_sorted = sorted(zip_ind_verts, key=lambda x:x[1][0])
    start_index = verts[verts_world_sorted[0][0]].index
    end_index = verts[verts_world_sorted[-1][0]].index
    sorted_verts = [bm.verts[start_index]]
    print("start index is {}, end index is {}".format(start_index, end_index))
    bm.verts[start_index].select = True  # start points 
    bm.verts[end_index].select = True  # end points
    cont=0

    while cont< len(verts):
        v=sorted_verts[cont]
        edges = v.link_edges

        for e in edges:
            if e.select:
                vn = e.other_vert(v)
                if vn not in sorted_verts:
                    sorted_verts.append(vn)
        cont+=1

    sorted_index = [v.index for v in sorted_verts]
    save_pickle_file(os.path.join(contour_path, file_name) , sorted_index)


if __name__ == "__main__":
    file_path = r"\\192.168.20.63\ai\Liyou_wang_data\cto_2020_03_18\bs_v0002\contour_v1"
    #choose_vertex(file_path)
    #select_verts(file_path)
    name = "mouth_down_contour_5"
    generate_contour(file_path, name)