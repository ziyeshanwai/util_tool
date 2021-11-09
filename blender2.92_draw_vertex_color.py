import bpy
import numpy as np
import random


def error2vertex_color(error):
    """
    error: n size return correspoinding error map
    """
#    n_color = error.shape[0]
    colors = error/error.max()
#    res = np.matmul(weight, colors)
    return colors

def add_vertex_color_to_mesh(ob):
    mat = bpy.data.materials.new(name='VertexColor')
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    vert_color = mat.node_tree.nodes.new(type="ShaderNodeVertexColor")  # set VertexColor

    bsdf.inputs[5].default_value = 0

    links = mat.node_tree.links
    links.new(vert_color.outputs[0], bsdf.inputs[0])
    
    if len(ob.data.materials):
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)
#    for obj in objs:
#        if len(obj.data.materials):
#            obj.data.materials[0] = mat
#        else:
#            obj.data.materials.append(mat)
#    
    return

def set_ob_vert_col(me, colors):
    """
    https://github.com/PeizhuoLi/neural-blend-shapes/blob/main/blender_scripts/vertex_color.py
    """
    vcols = me.data.vertex_colors
    polys = me.data.polygons
    vcol = vcols.new(name="Visualization")
    idx = 0
    for poly in polys:
        verts = poly.vertices
        for i, _ in enumerate(poly.loop_indices):
            c = colors[verts[i]]
#            print(c)
            vcol.data[idx].color = (c[0], c[1], c[2], 1.0)  # 0-1
#            vcol.data[idx].color = (random.random(), random.random(), random.random(), 1.0)
            idx += 1 


if __name__ == "__main__":
    print("--"*100)
    ob = bpy.data.objects["pose_0"]
    error = np.random.rand(len(ob.data.vertices), 3)
    color = error2vertex_color(error)
#    print(color)
    set_ob_vert_col(ob, color)
#    add_vertex_color_to_mesh(ob)