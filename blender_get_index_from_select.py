import bpy
import bmesh

obj=bpy.context.object
if obj.mode == 'EDIT':
    bm=bmesh.from_edit_mesh(obj.data)
    for v in bm.verts:
        if v.select:
            print(v.co)
else:
    print("Object is not in edit mode.")
    
# method 1

inds = [i.index for i in bpy.context.active_object.data.vertices if i.select]  

# method 2
inds = [i.index for i in bmesh.from_edit_mesh(bpy.context.active_object.data).verts if i.select]