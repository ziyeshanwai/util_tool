import bpy
import bmesh
bm = bmesh.new()
ob = bpy.context.active_object
bm.from_mesh(ob.data)

emptyMesh = bpy.data.meshes.new('emptyMesh')
theObj = bpy.data.objects.new("object_name", emptyMesh)
bpy.context.scene.collection.objects.link(theObj)
#bpy.data.collections["Collection 2"].objects.link(theObj)
bm.to_mesh(emptyMesh)
bm.free()