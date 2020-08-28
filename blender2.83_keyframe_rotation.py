import bpy
import os
import pickle
import sys
import json


def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))


def load_json(json_file):
    """
    load json file
    :param json_file: json 文件路径
    :return:
    """
    if os.path.exists(json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
    else:
        print("{} is not exits".format(json_file))
        data = None
    return data


if __name__ == '__main__':
    argv = sys.argv
    solver_file = argv[argv.index("-p") + 1]
    cfg = load_json(solver_file)
    output_path = cfg['output_path']
    fbx_output_path = output_path
    fbx_name = "{}.fbx".format("eye_animation")
    eye_weights_path = os.path.join(fbx_output_path, '{}.pkl'.format('bs_eye_ball'))
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(0, 0, 0),
                                         rotation=(1.5708, 0.0, 0.0))
    bpy.context.active_object.name = 'right_eye'
    bpy.ops.object.transform_apply()
    bpy.ops.mesh.primitive_uv_sphere_add(enter_editmode=False, align='WORLD', location=(4, 0, 0),
                                         rotation=(1.5708, 0.0, 0.0))
    bpy.context.active_object.name = 'left_eye'
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.ops.object.transform_apply()
    weights = load_pickle_file(eye_weights_path)
    for i in range(0, len(weights)):
        up, down, left, right = weights[i]
        bpy.data.objects['left_eye'].rotation_euler[0] = (-30 * up + 30 * down) / 180 * 3.14  # up down
        bpy.data.objects['left_eye'].rotation_euler[1] = 0
        bpy.data.objects['left_eye'].rotation_euler[2] = (-30 * right + 30 * left) / 180 * 3.14
        bpy.data.objects['left_eye'].keyframe_insert(data_path="rotation_euler", frame=i)
        bpy.data.objects['right_eye'].rotation_euler[0] = (-30 * up + 30 * down) / 180 * 3.14  # up down
        bpy.data.objects['right_eye'].rotation_euler[1] = 0
        bpy.data.objects['right_eye'].rotation_euler[2] = (-30 * right + 30 * left) / 180 * 3.14
        bpy.data.objects['right_eye'].keyframe_insert(data_path="rotation_euler", frame=i)
        if i % 100 == 0:
            print('insert frame {}'.format(i))
        # bpy.context.active_object.rotation_euler[0] = (-25*up + 25*down)/180 * 3.14 # up down
        # bpy.context.active_object.rotation_euler[1] = 0
        # bpy.context.active_object.rotation_euler[2] =  (-30*up + 30*down)/180 * 3.14
        # bpy.context.active_object.keyframe_insert(data_path="rotation_euler", frame=i)
    bpy.context.view_layer.objects.active = bpy.data.objects['left_eye']
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.context.view_layer.objects.active = bpy.data.objects['right_eye']
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')
    bpy.context.scene.frame_end = 0
    bpy.context.scene.frame_end = len(weights)
    bpy.data.objects['left_eye'].select_set(True)
    bpy.data.objects['right_eye'].select_set(True)
    bpy.ops.export_scene.fbx(filepath=os.path.join(output_path, fbx_name), check_existing=True,
                             filter_glob="*.fbx", use_selection=True, use_active_collection=False, global_scale=1.0,
                             apply_unit_scale=True, apply_scale_options='FBX_SCALE_NONE', bake_space_transform=False,
                             object_types={'MESH', 'ARMATURE'}, use_mesh_modifiers=False,
                             use_mesh_modifiers_render=True,
                             mesh_smooth_type='OFF', add_leaf_bones=True, use_armature_deform_only=False,
                             armature_nodetype='NULL', bake_anim=True, bake_anim_use_all_bones=True,
                             bake_anim_use_nla_strips=False, bake_anim_use_all_actions=True,
                             bake_anim_force_startend_keying=True, bake_anim_step=1.0, bake_anim_simplify_factor=1.0,
                             path_mode='AUTO', embed_textures=False, batch_mode='OFF', use_batch_own_dir=True,
                             use_metadata=True, axis_forward='-Z', axis_up='Y')
    print("export {} finish!".format(os.path.join(output_path, fbx_name)))