bl_info = {
    "name": "Vis Errors",
    "author": "Liyou Wang",
    "version": (1, 0),
    "blender": (2, 92, 0),
    "location": "View3D > Toolbar > Vis Erros",
    "description": "vis two object similarity",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}
 
 
 
import bpy
import numpy as np




def get_animation_verts(ob_name):
    obj = bpy.data.objects[ob_name]
    count = len(obj.data.vertices)
    verts = np.zeros(count*3, dtype=np.float32)
    depsgraph = bpy.context.evaluated_depsgraph_get()
    object_eval = obj.evaluated_get(depsgraph)
    mesh_from_eval = object_eval.to_mesh()
    b = mesh_from_eval.vertices.foreach_get("co", verts)
    #mesh_from_eval = bpy.data.meshes.new_from_object(object_eval)  # debug
    object_eval.to_mesh_clear()
    b = verts
    return  b


def error2rgb(e):
    h = np.clip(e, 0, bpy.context.scene.max_error)/bpy.context.scene.max_error
    r = 0.4*h
    g = h
    b = 1-0.5*h
    return r, g, b 


def set_vcols():
    i=0
    sob = bpy.context.scene.SourceOb
    tob = bpy.context.scene.TargetOb
    ob1v = get_animation_verts(sob).reshape(-1, 3)
    ob2v = get_animation_verts(tob).reshape(-1, 3)
    matrix_sob = np.array(bpy.data.objects[sob].matrix_world.to_3x3())
    matrix_tob = np.array(bpy.data.objects[tob].matrix_world.to_3x3())
    ob1v = matrix_sob.dot(ob1v.T).T
    ob2v = matrix_tob.dot(ob2v.T).T
    mesh = bpy.data.objects[sob].data
    color_layer = mesh.vertex_colors["Col"]
    e = np.linalg.norm(ob1v - ob2v, axis=1) * 10 # mm
    print("min:{} max:{}".format(e.min(), e.max()))
    for poly in mesh.polygons:
        for idx in poly.loop_indices:
            id = mesh.loops[idx].vertex_index
            r,g,b = error2rgb(e[id])
            a = 1
            color_layer.data[i].color = r,g,b,a
            i += 1


class WM_OT_vis_error(bpy.types.Operator):
    bl_label = "VIS ERROR"
    bl_idname = "wm.vis_error"

    def __init__(self) -> None:
        super().__init__()

    def my_handler(self, scene, context):
        frame = bpy.context.scene.frame_current
        print("current frame is {}".format(frame))
        set_vcols()

    def execute(self, context):
        bpy.app.handlers.frame_change_pre.append(self.my_handler)
        print("register bpy.app.handlers.frame_change_pre")
        return {'FINISHED'} 

    @classmethod
    def poll(cls, context):
        return context.mode=="OBJECT"  # 如果不是edit mode, 按钮会变成非激活状态


class WM_OT_clean_handler(bpy.types.Operator):
    bl_label = "Clean Handler"
    bl_idname = "wm.clean_handler"

    def execute(self, context):
        pre = bpy.app.handlers.frame_change_pre
        del pre[0:len(pre)]
        print("delet bpy.app.handlers.frame_change_pre")
        return {'FINISHED'} 

    #This is the Main Panel (Parent of Panel A and B)
class MainPanel(bpy.types.Panel):
    bl_label = "Vis Errors"
    bl_idname = "VIEW_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Vis Errors'
   
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
       
        scene = context.scene               
        layout.prop_search(scene, "SourceOb", scene, "objects")
        layout = self.layout
        layout.prop_search(scene, "TargetOb", scene, "objects")
        layout = self.layout
        layout.prop(scene, "max_error")
        layout = self.layout
        layout.operator("wm.vis_error", icon= 'CUBE', text= "vis error")
        layout = self.layout
        layout.operator("wm.clean_handler", icon= 'CUBE', text= "Clean Handler")



def register():
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(WM_OT_vis_error)
    bpy.utils.register_class(WM_OT_clean_handler)
    bpy.types.Scene.SourceOb = bpy.props.StringProperty()
    bpy.types.Scene.TargetOb = bpy.props.StringProperty()
    bpy.types.Scene.max_error = bpy.props.FloatProperty(name="max error",default=5.0, min=0.1, max=1000.0)
   
   
 
    #Here we are UnRegistering the Classes    
def unregister():
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(WM_OT_vis_error)
    bpy.utils.unregister_class(WM_OT_clean_handler)
    del bpy.types.Scene.SourceOb
    del bpy.types.Scene.TargetOb
    del bpy.types.Scene.max_error


if __name__ == "__main__":
    register()