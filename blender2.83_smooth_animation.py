import bpy

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
    