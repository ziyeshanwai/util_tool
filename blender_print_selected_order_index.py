import bpy, bmesh

print("*"*50)
oa = bpy.context.active_object
obj = bpy.context.object
#bpy.ops.mesh.shortest_path_select() #add for request
me = obj.data
bm = bmesh.from_edit_mesh(me)
v1 = [elem for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
index_order = [v.index for v in v1]
print("order index is {}".format(index_order))
verts_index = [v.index for v in bm.verts if v.select]
#cont=0
#while cont < len(verts_index):
#    v=v1[cont]
#    edges = v.link_edges
#    for e in edges:
#        if e.select:
#            vn = e.other_vert(v)
#            if vn not in v1:
#                list.append(vn)
#    cont+=1

#for v in list:
#    print(v.index)
#bmesh.update_edit_mesh(me, True)
