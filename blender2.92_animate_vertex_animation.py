"""
https://blender.stackexchange.com/questions/1042/how-to-animate-vertex-color-of-an-object
"""
import bpy
import random



global obj
obj = bpy.data.objects["Cube"]
global mesh
mesh = obj.data
global color_layer
color_layer = mesh.vertex_colors["Col"]
def set_vcols(frame, obj, mesh, color_layer):
    i=0
    for poly in mesh.polygons:
        
        for idx in poly.loop_indices:
            tmp = random.random()
            r = tmp
            g = 0.5
            b = 0.5
            a = 1
            color_layer.data[i].color = r,g,b,a
            i += 1
            

def my_handler(scene):
    frame = scene.frame_current
    print("current frame is {}".format(frame))
    
    set_vcols(frame, obj, mesh, color_layer)

bpy.app.handlers.frame_change_pre.append(my_handler)