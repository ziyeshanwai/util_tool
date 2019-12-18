# assuming the object is currently in Edit Mode.
import bpy
import bmesh

if __name__ == "__main__":

    obj = bpy.context.edit_object
    me = obj.data
    bm = bmesh.from_edit_mesh(me)
    print("print the selected points index")
    for f in bm.verts:
        if f.select:
            print(f.index)
    print("print selected face index")
    for f in bm.faces:
        if f.select:
            print(f.index)        
        
    """
    #print face index
    for f in bm.faces:
        if f.select:
            print(f.index)
    """

    # Show the updates in the viewport
    # and recalculate n-gon tessellation.
    #bmesh.update_edit_mesh(me, True)