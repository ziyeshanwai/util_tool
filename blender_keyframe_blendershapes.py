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
    
    blendshapes_path = r"\\192.168.20.63\ai\Liyou_wang_data\new_version_blendshapes\xiaoyue\selected_face"
    fbx_output_path = r"\\192.168.20.63\ai\Liyou_wang_data\faceGood\morph"
    fbx_name = "{}.fbx".format("xiaoyue")
    if os.path.exists(os.path.join(blendshapes_path,  "names.pkl")):
        filenames = load_pickle(os.path.join(blendshapes_path,  "names.pkl"))
    else:
        filenames = os.listdir(blendshapes_path)
    base_mesh_name = "head_geo.obj"
   
    for file in filenames:
        if file.endswith(".obj"):
            bpy.ops.import_scene.obj(filepath=os.path.join(blendshapes_path, file))
            bpy.context.selected_objects[0].name = file[:-4]
    for obj in bpy.context.scene.objects:
        obj.select_set(True)
            
    #bpy.data.objects[base_mesh_name[:-4]].select=True
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
    bpy.context.view_layer.objects.active = bpy.data.objects[base_mesh_name[:-4]]
    bpy.ops.object.join_shapes()
    bpy.data.objects[base_mesh_name[:-4]].select_set(False)
    bpy.ops.object.delete()
    bpy.ops.export_scene.fbx(filepath=os.path.join(fbx_output_path, fbx_name), check_existing=True, axis_forward='-Z', axis_up='Y')
  
    weights_list_path = os.path.join(r"\\192.168.20.63\ai\Liyou_wang_data\new_version_blendshapes\xiaoyue\blendshape127", "weights_list.pkl")
    weights_list = load_pickle(weights_list_path)
    bpy.context.view_layer.objects.active = bpy.data.objects[base_mesh_name[:-4]]
    ob = bpy.context.active_object
    
    filenames.remove(base_mesh_name)
    for frame in range(0, 1921):
        weight = weights_list[frame]
        print("insert frame {}".format(frame))
        for i, file in enumerate(filenames):
            ob.data.shape_keys.name = "key"
            #bpy.data.shape_keys[0].key_blocks[file[:-4]]..slider_min = -1 
            ob.data.shape_keys.key_blocks[file[:-4]].value=weight[i, 0]
            ob.data.shape_keys.key_blocks[file[:-4]].keyframe_insert("value", frame=frame)
            
    """
    for frame in range(0, 1921):
        weight = weights_list[frame]
        print("insert frame {}".format(frame))
        for shapekey in bpy.data.shape_keys:
            for i, keyblock in enumerate(shapekey.key_blocks):
                if keyblock.name != 'Basis':
                    #keyblock.slider_min = -1  # 最小值是-1
                    keyblock.value = weight[i-1, 0]
                    keyblock.keyframe_insert("value", frame=frame)
    """
    bpy.data.objects[base_mesh_name[:-4]].select_set(True)
    bpy.context.view_layer.objects.active = bpy.data.objects[base_mesh_name[:-4]]
    bpy.ops.nla.bake(frame_start=0, frame_end=len(weights_list), only_selected=True, visual_keying=False, clear_constraints=False, use_current_action=False, bake_types={'OBJECT'})
    #print("bake action finished")
    bpy.ops.export_scene.fbx(filepath=os.path.join(blendshapes_path, fbx_name), check_existing=True, filter_glob="*.fbx", use_selection=False, use_active_collection=False, global_scale=1.0, apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', bake_space_transform=False, object_types={'MESH'}, use_mesh_modifiers=False, use_mesh_modifiers_render=True, mesh_smooth_type='OFF', add_leaf_bones=False, use_armature_deform_only=False, armature_nodetype='NULL', bake_anim=True, bake_anim_use_all_bones=True, bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True, bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0, path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True, use_metadata=True, axis_forward='-Z', axis_up='Y')
    print("export animation {} finished".format(os.path.join(blendshapes_path, fbx_name)))
    
    """
    #生成完后记得使用object-->animation-->BakeAction bake 一次动画才行 再导出动画
    
    