"""
https://blender.stackexchange.com/questions/36905/uv-coordinates-to-xyz-coordinates
"""

import bpy
import bmesh
from mathutils.geometry import barycentric_transform, intersect_point_tri_2d
from mathutils import Vector


def map_flat_pt_to_face(flat_pt, uv_layer, face):
    pa, pb, pc = [l[uv_layer].uv.to_3d() for l in face.loops]
    pd, pe, pf = [v.co for v in face.verts]
    return barycentric_transform(flat_pt, pa, pb, pc, pd, pe, pf)


def objHash(bMeshObj):
    return hash(repr([v.co for v in bMeshObj.verts]))


rivetMeshCache = {}

def UVto3dSpace(uv, objectName, uv_layer, worldSpace=True):
    global rivetMeshCache
    
    # Get the mesh
    ob = bpy.data.objects[objectName]
    mesh = ob.data
    
    # Put the UV point on a flat plane
    puv = Vector([uv[0], uv[1], 0.0])
    
    # Get new bmesh version of mesh
    bm = bmesh.new()
    #bm.from_mesh(mesh)
    bm.from_object(ob, bpy.context.evaluated_depsgraph_get())  # Account for deformations
    
    # Check for a cached bmesh before triangulating a new one
    checkForMesh = mesh.name in rivetMeshCache
    #if (checkForMesh and mesh.is_updated_data):
    #print(objHash(bm))n
    if (checkForMesh and rivetMeshCache[mesh.name][1] == objHash(bm)):
        bm = rivetMeshCache[mesh.name][0]
        #print("Using old mesh", mesh.is_updated_data)
    else:
        if checkForMesh:
            # Clear memory of existing cache
            rivetMeshCache[mesh.name][0].free()
        

        # Triangulate the mesh (so we're just dealing with triangles)
#        bmesh.ops.triangulate(bm, faces=bm.faces, quad_method=1, ngon_method=1)
        
        # Store the mesh for next time
        rivetMeshCache[mesh.name] = [bm, objHash(bm)]
        #print("Using new mesh")

    # Get the UV layer
    uv_layer = bm.loops.layers.uv['UVMap']

    # Iterate faces, return the mapped position in the first (UV) triangle that 'intersects'
    for face in bm.faces:
        pa, pb, pc = [l[uv_layer].uv.to_3d() for l in face.loops]
        if intersect_point_tri_2d(puv, pa, pb, pc):
            localPos = map_flat_pt_to_face(puv, uv_layer, face)
            break
    else:
        # If the point hit empty space (no UV triangles), just use the origin (may use last valid point instead later)
        localPos = Vector([0.0, 0.0, 0.0])
    
    # Return the position in world space if specified
    if worldSpace:
        return ob.matrix_world@localPos
    else:
        return localPos


if __name__ == "__main__":
    ob = bpy.data.objects["wraped_ob"]

    for area in bpy.context.screen.areas:
        if area.type == 'IMAGE_EDITOR':   #find the UVeditor
            cursor = area.spaces.active.cursor_location   # get cursor location
            print(cursor)
#        if  area.spaces.active.image :                #get image dimension
#            x = area.spaces.active.image.size[0]
#            y = area.spaces.active.image.size[1]
#        else:
#            x = y = 256

#        for v in ob.data.loops :
#             uv = ob.data.uv_layers.active.data[v.index].uv   #get uv coo

#            #calculate and print the position in the uv editor
#             print("vertex %d at with UV coo (%d , %d) at  (%d ,%d)"%(v.index, uv[0], uv[1], uv[0]*x, uv[1]*y) )  
#             print( "is selected ? " , ob.data.uv_layers.active.data[v.index].select )

#        print (cursor,x,y)
    world_co = UVto3dSpace(cursor, ob.name, None)
    print("world co is {}".format(world_co))
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.mesh.primitive_uv_sphere_add(radius=0.1, enter_editmode=False, align='WORLD', location=(world_co[0], world_co[1], world_co[2]), scale=(1, 1, 1))
    bpy.context.active_object.show_name = True
    bpy.context.active_object.select_set(False)
    bpy.context.view_layer.objects.active = ob
    bpy.context.active_object.select_set(True)
    bpy.ops.object.mode_set(mode='EDIT')