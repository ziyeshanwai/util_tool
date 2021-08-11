"""
http://wiki.theprovingground.org/blender-py-mesh
"""

import bpy
 
#Define vertices and faces
verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0)]
faces = [(0,1,2,3)]
 
# Define mesh and object variables
mymesh = bpy.data.meshes.new("Plane")
myobject = bpy.data.objects.new("Plane", mymesh)  
 
#Set location and scene of object
myobject.location = bpy.context.scene.cursor.location
bpy.context.scene.collection.objects.link(myobject)
 
#Create mesh
mymesh.from_pydata(verts,[],faces)
mymesh.update(calc_edges=True)

 
#Define vertices, faces, edges
verts = [(0,0,0),(0,5,0),(5,5,0),(5,0,0),(0,0,5),(0,5,5),(5,5,5),(5,0,5)]
faces = [(0,1,2,3), (4,5,6,7), (0,4,5,1), (1,5,6,2), (2,6,7,3), (3,7,4,0)]
 
#Define mesh and object
mymesh = bpy.data.meshes.new("Cube")
myobject = bpy.data.objects.new("Cube", mymesh)
 
#Set location and scene of object
myobject.location = bpy.context.scene.cursor.location
bpy.context.scene.collection.objects.link(myobject)
 
#Create mesh
mymesh.from_pydata(verts,[],faces)
mymesh.update(calc_edges=True)