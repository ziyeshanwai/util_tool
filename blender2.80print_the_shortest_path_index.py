import bpy
import bmesh

ob = bpy.context.object
me = ob.data
bm = bmesh.from_edit_mesh(me)
bpy.ops.mesh.select_all(action='DESELECT')
start_index = 5017
end_index = 2045
bm.verts[start_index].select = True  # start points 
bm.verts[end_index].select = True  # end points
bpy.ops.mesh.shortest_path_select()
#bmesh.update_edit_mesh(me, False, False)
#print(len(bm.select_history))
#v1,v2 = [elem for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
#ind = [elem.index for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
list = [bm.verts[start_index]]
verts = [v for v in bm.verts if v.select]
print("len(vertes) is {}".format(len(verts)))

cont=0

while cont< len(verts):
    v=list[cont]
    edges = v.link_edges

    for e in edges:
        if e.select:
            vn = e.other_vert(v)
            if vn not in list:
                list.append(vn)
    cont+=1

for v in list:
    print(v.index)
#bmesh.update_edit_mesh(me, True) 

#bmesh.update_edit_mesh(me, False, False)