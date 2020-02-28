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
print("method 1 id is {}".format(inds))
# method 2
inds = [i.index for i in bmesh.from_edit_mesh(bpy.context.active_object.data).verts if i.select]
print("method2 id is {}".format(inds))

print("cursor global position is {}".format(bpy.context.scene.cursor.location))

"""
a demo show the conversion between global coordinates and local coordinates
matrix multiply vector use @
"""
global_coord = obj.matrix_world.translation
print("global coor is {}".format(global_coord))
local_coord = obj.matrix_world.inverted() @ global_coord
print("local coor is {}".format(local_coord))

print("cursor local position is {}".format(obj.matrix_world.inverted() @ bpy.context.scene.cursor.location))