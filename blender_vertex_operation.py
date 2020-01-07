import bpy
import mathutils

obj = bpy.context.active_object
v = obj.data.vertices[0]
print("v is {}".format(v.co))  # v.co store the obj coordinates

co_final = obj.matrix_world @ (v.co + mathutils.Vector([1,2,3]))
v.co = v.co - mathutils.Vector([1,2,3])

# now we can view the location by applying it to an object
#obj_empty = bpy.data.objects.new("Test", None)
#bpy.context.collection.objects.link(obj_empty)
#obj_empty.location = co_final

if obj.mode == 'EDIT':
    # this works only in edit mode,
    bm = bmesh.from_edit_mesh(obj.data)
    verts = [vert.co for vert in bm.verts]

else:
    # this works only in object mode,
    verts = [vert.co for vert in obj.data.vertices]

# coordinates as tuples
plain_verts = [vert.to_tuple() for vert in verts]
selectedVerts = [v for v in bpy.context.active_object.data.vertices if v.select]

for vert in selectedVerts:
    print(vert.co)
    vert.co = mathutils.Vector([1,2,3]) # 这种赋值要在obj模式下
    
