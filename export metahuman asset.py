# metahuman plugin
import bpy
import os
import json

def load_json(json_file):
    """
    load json file
    :param json_file: json 文件路径
    :return:
    """
    with open(json_file, 'r') as f:
        data = json.load(f)
    return data


def export_bs_obj():
    names_json = r"E:\UE4_project\ouput_json\curve_names.json"
    outputpath = r""
    names = load_json(names_json)
    scene = bpy.context.scene
    for frame in range(scene.frame_start, scene.frame_end):
        scene.frame_set(frame)
        bpy.context.view_layer.update()
        the_file = names['names'][frame] + '.obj'
        print("the fiile is {}".format(the_file))
        bpy.ops.export_scene.obj(filepath=os.path.join(outputpath, the_file), check_existing=True, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl", use_selection=True, use_animation=False, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=False, use_uvs=False, use_materials=False, use_triangles=False, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=True, global_scale=1.0, path_mode='AUTO')
    
def generage_blendshape():
    names_json = r"E:\curve_names.json"
    bs_path = r""
    file_names_dict = load_json(names_json)
    filenames = file_names_dict["names"]
    for file in filenames:
        filename = "{}.obj".format(file)
        if os.path.exists(os.path.join(bs_path, filename)):
            bpy.ops.import_scene.obj(filepath=os.path.join(bs_path, filename))
            bpy.context.selected_objects[0].name = file
    for obj in bpy.context.scene.objects:
        obj.select_set(True)
            
    #bpy.data.objects[base_mesh_name[:-4]].select=True
    bpy.context.view_layer.objects.active = bpy.context.selected_objects[-1]
    bpy.context.view_layer.objects.active = bpy.data.objects[filenames[0]]
    bpy.ops.object.join_shapes()
    bpy.data.objects[filenames[0]].select_set(False)
    bpy.ops.object.delete()
    
    
def key_frame():
    animaiton_path = os.path.join(r"E:\UE4_project\ouput_json", "output_ani.json")
    ani = load_json(animaiton_path)
    for shapekey in bpy.data.shape_keys:
            for i, keyblock in enumerate(shapekey.key_blocks):
                if keyblock.name != 'Basis':
                    
                    print("keyblock.name {}".format(keyblock.name))
                    if keyblock.name in ani.keys():
                        for f in range(0, len(ani[keyblock.name])):
                            keyblock.value = ani[keyblock.name][f]["value"]
                            frame = ani[keyblock.name][f]["frame_number"]
                            keyblock.keyframe_insert("value", frame=frame)

if __name__ == "__main__":
#    generage_blendshape()

    key_frame()
