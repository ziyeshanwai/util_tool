import bpy
import bmesh
import os

"""
auto choose start and end points
"""
def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))
contour_path = r"\\192.168.20.63\ai\Liyou_wang_data\cto_2020_03_18\bs_v0002\contour_data"
file_name = "{}.pkl".format("test")
ob = bpy.context.object
me = ob.data
bm = bmesh.from_edit_mesh(me)
bpy.ops.mesh.select_all(action='DESELECT')
#bpy.ops.mesh.shortest_path_select()
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