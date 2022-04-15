"""
print shortes path index
https://blender.stackexchange.com/questions/69796/selection-history-from-shortest-path
"""
import bpy, bmesh

ob = bpy.context.active_object
#obj = bpy.context.object

#bpy.ops.mesh.shortest_path_select() #add for request

me = ob.data
bm = bmesh.from_edit_mesh(me)


v1 = [elem for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
verts_list = v1
num = len([v.index for v in bm.verts if v.select])
print("num is  {}".format(num))
print(len(verts_list))
cont=0

while cont< num:
    
    v = verts_list[cont]
    edges = v.link_edges

    for e in edges:
        if e.select:
            vn = e.other_vert(v)
            if vn not in verts_list:
                verts_list.append(vn)

    cont+=1

ind = [v.index for v in verts_list]
print(list(reversed(ind)))
#for v in verts_list.reverse():
#    print(v.index)
bmesh.update_edit_mesh(me, True) 