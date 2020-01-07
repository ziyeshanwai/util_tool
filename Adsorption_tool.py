import bpy
import mathutils
import bmesh
import numpy as np

reference_obj = bpy.data.objects["head_geo.001"] # reference obj name
obj = bpy.context.active_object
obj.data.vertices[0].co = mathutils.Vector([0,0,0])  # can not assign value directly

if obj.mode == 'EDIT':  # this method can gennerate effect in edit 
    # this works only in edit mode,
    bm = bmesh.from_edit_mesh(obj.data)
    verts = [vert for vert in bm.verts if vert.select]
    verts_index = [vert.index for vert in bm.verts if vert.select]
    for i, vert in enumerate(verts):
        #print(obj.data.vertices[ind].co )
        vert.co = reference_obj.data.vertices[verts_index[i]].co
        #print(obj.data.vertices[ind].co )
    print("finish")