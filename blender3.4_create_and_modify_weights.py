import bpy
import random
import numpy as np

bpy.app.handlers.frame_change_post.clear()
def weight_changer(scene, depsgraph):
    ob = bpy.context.active_object
    #new_vertex_group = ob.vertex_groups.new(name='_GROUP_NAME_')
    new_vertex_group=ob.vertex_groups["_GROUP_NAME_"]
    vertex_group_data = [i for i in range(0, len(ob.data.vertices))]
    new_vertex_group.add(vertex_group_data, 1.0, 'ADD')
    vertex_indices = np.random.randint(0, 200, 200).tolist()
    new_vertex_group.add( vertex_indices, np.random.rand(1)[0], 'REPLACE' )

bpy.app.handlers.frame_change_post.append(weight_changer)
