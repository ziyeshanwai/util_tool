import bpy
import bgl
import blf
import mathutils
import bmesh
 
obj_data =  bpy.context.active_object.data
bm = bmesh.from_edit_mesh(obj_data)
vert_layer = bm.verts.layers.int.new('id')
my_id = bm.verts.layers.int['id']

#access
bm.verts[0][my_id] = 42

#apply the changes
bmesh.update_edit_mesh(bpy.context.active_object.data)

print(bm.verts[0][my_id])