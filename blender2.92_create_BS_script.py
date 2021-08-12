import bpy
import bmesh
import numpy as np

def generate_newobject(name, from_ob):
    """
    using bmesh generate new object, then use numpy foreach_set set vertice position
    """
    bm = bmesh.new()
    bm.from_mesh(from_ob.data)
    emptyMesh = bpy.data.meshes.new(name)
    theObj = bpy.data.objects.new(name, emptyMesh)
    bpy.context.scene.collection.objects.link(theObj)
    bm.to_mesh(emptyMesh)
    bm.free()
    theObj.rotation_euler = from_ob.rotation_euler
    return theObj

def set_ob_vertice(ob, verts_np):
    """
    set obj vertex
    """
    
    ob.data.vertices.foreach_set('co', verts_np)
    ob.data.update()

def get_current_ob_vertice(ob):
    """
    get current ob vertices 
    """
    count = len(ob.data.vertices)
    verts = np.zeros(count*3, dtype=np.float32)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = ob.evaluated_get(depsgraph)
    mesh_from_eval = object_eval.to_mesh()
    b = mesh_from_eval.vertices.foreach_get("co", verts)
    object_eval.to_mesh_clear()
    return verts
    
def generate_random_shapekey_main():
    bpy.context.scene.frame_current = bpy.context.scene.frame_start # move to first frame
    ob_name = "ProjectShan_sequence.001"
    ob = bpy.data.objects[ob_name]
    new_ob_0 = generate_newobject("test", ob)
    verts_np = get_current_ob_vertice(ob)
    set_ob_vertice(new_ob_0, verts_np)
    bpy.context.scene.frame_current = bpy.context.scene.frame_start + 281
    new_ob_1 = generate_newobject("test1", ob)
    verts_np = get_current_ob_vertice(ob)
    set_ob_vertice(new_ob_1, verts_np)
    
def add_shapekey(ob, shapkeyname, verts_np):
    if ob.data.shape_keys: ## exist shapkey
        tmp = ob.shape_key_add()
        tmp.name = shapkeyname
    else:
        tmp = ob.shape_key_add()
        tmp.name = "Basis"
        tmp = ob.shape_key_add()
        tmp.name = shapkeyname
    tmp.data.foreach_set('co', verts_np)
    tmp.data.update()
    
if __name__ == "__main__":
    generate_random_shapekey_main()
    ob_name = "test"
    ob = bpy.data.objects[ob_name]
    count = len(ob.data.vertices)
    verts_np = np.zeros(count * 3, dtype=np.float32)
    bpy.data.objects["test1"].data.vertices.foreach_get('co', verts_np)
    add_shapekey(ob, "key1", verts_np)