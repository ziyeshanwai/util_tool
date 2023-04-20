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


import bpy
import json
import os


def _load_json(json_file):
    """
    load json file
    :param json_file: json 文件路径
    :return:
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    json_path = os.path.join(r"D:\pycharm_projects\BSGECMD\CODE\MASK", "CTRL_expressions_eyeBlinkL.json")
    data = _load_json(json_path)
    ob = bpy.context.active_object
    new_vertex_group = ob.vertex_groups.new(name="CTRL_expressions_eyeBlinkL")
    vertex_group_data = [i for i in range(0, len(ob.data.vertices))]
    new_vertex_group.add(vertex_group_data, 1.0, 'ADD')
#    vertex_indices = np.random.randint(0, 200, 200).tolist()
    for i, v in enumerate(data['data']):
        new_vertex_group.add( [i], v, 'REPLACE' )
