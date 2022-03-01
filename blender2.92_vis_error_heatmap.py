"""
https://blender.stackexchange.com/questions/1042/how-to-animate-vertex-color-of-an-object
"""
import bpy
import random
import numpy as np



global obj
obj = bpy.data.objects["fit"]
global mesh
mesh = obj.data
global color_layer
color_layer = mesh.vertex_colors["Col"]



def get_animation_verts(ob_name):
    obj = bpy.data.objects[ob_name]
    count = len(obj.data.vertices)
    verts = np.zeros(count*3, dtype=np.float32)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = obj.evaluated_get(depsgraph)
    mesh_from_eval = object_eval.to_mesh()
    b = mesh_from_eval.vertices.foreach_get("co", verts)
    #mesh_from_eval = bpy.data.meshes.new_from_object(object_eval)  # debug
    object_eval.to_mesh_clear()
    b = verts
    return b


def set_vcols(frame, obj, mesh, color_layer):
    i=0
    ob1v = get_animation_verts("seq").reshape(-1, 3)
    ob2v = get_animation_verts("fit").reshape(-1, 3)
    e = np.linalg.norm(ob1v - ob2v, axis=1) * 10
    print("min:{} max:{}".format(e.min(), e.max()))
    for poly in mesh.polygons:
        for idx in poly.loop_indices:
            id = mesh.loops[idx].vertex_index
            r,g,b = error2rgb(e[id])
            a = 1
            color_layer.data[i].color = r,g,b,a
            i += 1

def error2rgb(e):
    h = np.clip(e, 0, 5)/5
    r = 0.4*h
    g = h
    b = 1-0.5*h
    return r, g, b
                

def my_handler(scene):
    frame = scene.frame_current
    print("current frame is {}".format(frame))
    set_vcols(frame, obj, mesh, color_layer)

bpy.app.handlers.frame_change_pre.append(my_handler)

"""
run the below code from console, then rerun your script
pre = bpy.app.handlers.frame_change_pre
del pre[0:len(pre)]
"""
"""
ob = bpy.data.objects["seq"]
mesh = ob.data
idxs = [idx for poly in mesh.polygons for idx in poly.loop_indices ]
idxs_array = np.array(idxs, dtype=np.float32)
"""