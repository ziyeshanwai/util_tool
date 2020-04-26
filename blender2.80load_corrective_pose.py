import pickle
import bpy
import os
import numpy as np


def load_pickle(path):
    with open(path, "rb") as f:
        weights_list = pickle.load(f)
    return weights_list



if __name__ == "__main__":
    """
    remove all the obj in the scene
    """
    
    blendshapes_path = r"\\192.168.20.63\ai\double_camera_data\2020-03-18\154524\slide_output_6\all_bs"
    weights_list_path = r"\\192.168.20.63\ai\double_camera_data\2020-03-18\154524\slide_output_6\weights_final"
    
    if os.path.exists(os.path.join(weights_list_path,  "names_combined_corrective.pkl")):
        filenames = load_pickle(os.path.join(weights_list_path,  "names_combined_corrective.pkl"))
    else:
        filenames = os.listdir(blendshapes_path)
    print("file names is {}".format(filenames))
    base_mesh_name = "head_geo.obj"
    
    for file in filenames:
        if file.endswith(".obj"):
            bpy.ops.import_scene.obj(filepath=os.path.join(blendshapes_path, file), use_split_objects=False,split_mode='OFF')
            bpy.context.selected_objects[0].name = file[:-4]
    
    for obj in bpy.context.scene.objects:
        if obj.name + ".obj" in filenames:
            obj.select_set(True)
    
    bpy.context.view_layer.objects.active = bpy.data.objects[base_mesh_name[:-4]]
    bpy.ops.object.join_shapes()
    bpy.data.objects[base_mesh_name[:-4]].select_set(False)
    bpy.ops.object.delete()

    weights_list_path = os.path.join(weights_list_path, "weights_combined_corrective.pkl")
    weights_list = load_pickle(weights_list_path)
    weights = np.array(weights_list, dtype=np.float32)
    slid_max = np.max(weights, axis = 0)
    slid_min = np.min(weights, axis = 0)
    bpy.context.view_layer.objects.active = bpy.data.objects[base_mesh_name[:-4]]
    ob = bpy.context.active_object
    filenames.remove(base_mesh_name)
    for frame in range(0, len(weights_list)):
        weight = weights_list[frame]
        print("insert frame {}".format(frame))
        for i, file in enumerate(filenames):
            ob.data.shape_keys.name = "key"
            if slid_max[i] > 1:
                bpy.data.shape_keys[0].key_blocks[file[:-4]].slider_max = slid_max[i]
            if slid_min[i] < 0:
                bpy.data.shape_keys[0].key_blocks[file[:-4]].slider_min = slid_min[i]
            ob.data.shape_keys.key_blocks[file[:-4]].value=weight[i, 0]
            ob.data.shape_keys.key_blocks[file[:-4]].keyframe_insert("value", frame=frame)
    """        
    bpy.data.objects[base_mesh_name[:-4]].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[base_mesh_name[:-4]]
    bpy.ops.nla.bake(frame_start=0, frame_end=len(weights_list), only_selected=True, visual_keying=False, clear_constraints=False, use_current_action=False, bake_types={'OBJECT'})
    """