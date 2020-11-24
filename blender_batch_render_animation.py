import bpy
import os
import sys


def ini_render_settings():
    print("initial render setting")
    bpy.context.scene.unit_settings.scale_length = 0.01
    bpy.context.scene.render.image_settings.file_format = 'FFMPEG'
    bpy.context.scene.render.ffmpeg.format = 'MPEG4'
    bpy.context.scene.render.ffmpeg.constant_rate_factor = 'MEDIUM'
    bpy.context.scene.render.ffmpeg.codec = 'H264'
    bpy.context.scene.render.fps = 60

    
def set_frame_number():
    start_number = bpy.data.objects['head_geo'].animation_data.action.frame_range[0]
    end_number = bpy.data.objects['head_geo'].animation_data.action.frame_range[1]
    bpy.context.scene.frame_start = start_number
    bpy.context.scene.frame_end = end_number
    
    
def adjust_view():
    for area in bpy.context.screen.areas:
        if area.type == "VIEW_3D":
            break

    for region in area.regions:
        if region.type == "WINDOW":
            break
    space = area.spaces[0]
    context = bpy.context.copy()
    context['area'] = area
    context['region'] = region
    context['space_data'] = space
    
    bpy.ops.view3d.view_selected(context)
    bpy.ops.view3d.view_axis(context, type='FRONT')
    context['space_data'].overlay.show_overlays = False

def render_animation(output_path):
    
    for i in range(1, len(bpy.data.objects['head_geo'].data.shape_keys.key_blocks)):
        bpy.data.objects['head_geo'].data.shape_keys.key_blocks[i].slider_min = -5
        bpy.data.objects['head_geo'].data.shape_keys.key_blocks[i].slider_max = 5
    set_frame_number()
    bpy.context.scene.render.filepath = output_path
    adjust_view()
    bpy.ops.render.opengl(animation=True)
    bpy.data.objects['head_geo'].select_set(True)
    bpy.ops.object.delete(use_global=False)


def import_fbx(file):
    bpy.ops.import_scene.fbx(filepath=input_path, global_scale=0.01) # bas
    bpy.context.selected_objects[0].name ='head_geo'

if __name__ == "__main__":
    input_dir = 
    print("input_dir is {}".format(input_dir))
    output_dir = 
    print("output_dir is {}".format(output_dir))
    ini_render_settings()
    names = os.listdir(input_dir)
    for name in names:
        input_path = os.path.join(input_dir, name)
        import_fbx(input_path)
        output_path = os.path.join(output_dir, name[:-3]+'mp4')
        render_animation(output_path)