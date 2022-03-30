"""
https://stackoverflow.com/questions/20792445/calculate-rgb-value-for-a-range-of-values-to-create-heat-map
"""

import bpy
import random
import numpy as np



global obj
obj = bpy.data.objects["controller"]
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
    ob1v = get_animation_verts("4d").reshape(-1, 3)
    ob2v = get_animation_verts("controller").reshape(-1, 3)
    e = np.linalg.norm(ob1v - ob2v, axis=1) * 10
    print("min:{} max:{}".format(e.min(), e.max()))
    for poly in mesh.polygons:
        for idx in poly.loop_indices:
            id = mesh.loops[idx].vertex_index
            r,g,b = convert_to_rgb(0, 5, e[id])
            a = 1
            color_layer.data[i].color = r,g,b,a
            i += 1

def convert_to_rgb0(minimum, maximum, value):
    minimum, maximum = float(minimum), float(maximum)
    value = np.clip(value, minimum, maximum)    
    halfmax = (minimum + maximum) / 2
    if minimum <= value <= halfmax:
        r = 0
        g = int( 255./(halfmax - minimum) * (value - minimum))
        b = int( 255. + -255./(halfmax - minimum)  * (value - minimum))
        return (r/255.0,g/255.0,b/255.0)    
    elif halfmax < value <= maximum:
        r = int( 255./(maximum - halfmax) * (value - halfmax))
        g = int( 255. + -255./(maximum - halfmax)  * (value - halfmax))
        b = 0
        return (r/255.0,g/255.0,b/255.0)
    
def convert_to_rgb(minimum, maximum, value):
    value = np.clip(value, minimum, maximum)
    minimum, maximum = float(minimum), float(maximum)
    ratio = 2 * (value-minimum) / (maximum - minimum)
    b = int(max(0, 255*(1 - ratio)))
    r = int(max(0, 255*(ratio - 1)))
    g = 255 - b - r
    return (r/255.0,g/255.0,b/255.0)
                

def my_handler(scene):
    frame = scene.frame_current
    print("current frame is {}".format(frame))
    set_vcols(frame, obj, mesh, color_layer)

bpy.app.handlers.frame_change_pre.append(my_handler)