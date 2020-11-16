import bpy

for window in bpy.context.window_manager.windows:
    screen = window.screen

for area in screen.areas:
    if area.type == 'VIEW_3D':
        override = {'window': window, 'screen': screen, 'area': area}
        bpy.ops.screen.screen_full_area(override)
        break


def smooth_curves():
    """
    smooth key
    """
    bpy.context.area.ui_type = 'FCURVES'
    bpy.ops.graph.select_all(action='SELECT');
    bpy.ops.graph.smooth()
    

if __name__ == '__main__':
    bpy.data.objects['head_geo'].select_set(True) # this is very important
    bpy.context.view_layer.objects.active = bpy.data.objects['head_geo']
    smooth_curves()
    