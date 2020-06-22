bl_info = {
    "name": "Object Adder",
    "author": "Darkfall",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Toolbar > Object Adder",
    "description": "Adds objects and other functions",
    "warning": "",
    "wiki_url": "",
    "category": "Add Mesh",
}
 
 
 
import bpy
 
 
 
 
    #This is the Main Panel (Parent of Panel A and B)
class MainPanel(bpy.types.Panel):
    bl_label = "Object Adder"
    bl_idname = "VIEW_PT_MainPanel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Adder'
   
    def draw(self, context):
        layout = self.layout
        layout.scale_y = 1.2
       
        row = layout.row()
        row.label(text= "Add an object", icon= 'OBJECT_ORIGIN')
        row = layout.row()
        row.operator("wm.myop", icon= 'CUBE', text= "Cube")
        row.operator("mesh.primitive_uv_sphere_add", icon= 'SPHERE', text= "Sphere")
        row.operator("mesh.primitive_monkey_add", icon= 'MESH_MONKEY', text= "Suzanne")
        row = layout.row()
        row.operator("curve.primitive_bezier_curve_add", icon= 'CURVE_BEZCURVE', text= "Bezier Curve")
        row.operator("curve.primitive_bezier_circle_add", icon= 'CURVE_BEZCIRCLE', text= "Bezier Circle")
       
       
        row = layout.row()
        row.operator("object.text_add", icon= 'FILE_FONT', text= "Add Font")
        row = layout.row()
       
       
       
 
 
 
    #This is Panel A - The Scale Sub Panel (Child of MainPanel)
class PanelA(bpy.types.Panel):
    bl_label = "Scale"
    bl_idname = "VIEW_PT_PanelA"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Adder'
    bl_parent_id = 'VIEW_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}
   
    def draw(self, context):
        layout = self.layout
        obj = context.object
       
        row = layout.row()
        row.label(text= "Select an option to scale your", icon= 'FONT_DATA')
        row = layout.row()
        row.label(text= "      object.")
        row = layout.row()
        row.operator("transform.resize")
        row = layout.row()
        layout.scale_y = 1.2
       
        col = layout.column()
        col.prop(obj, "scale")
       
       
       
 
 
 
    #This is Panel B - The Specials Sub Panel (Child of MainPanel)
class PanelB(bpy.types.Panel):
    bl_label = "Specials"
    bl_idname = "VIEW_PT_PanelB"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Object Adder'
    bl_parent_id = 'VIEW_PT_MainPanel'
    bl_options = {'DEFAULT_CLOSED'}
   
    def draw(self, context):
        layout = self.layout
       
        row = layout.row()
        row.label(text= "Select a Special Option", icon= 'COLOR_BLUE')
        row = layout.row()
        row.operator("object.shade_smooth", icon= 'MOD_SMOOTH', text= "Set Smooth Shading")
        row.operator("object.subdivision_set", icon= 'MOD_SUBSURF', text= "Add Subsurf")
        row = layout.row()
        row.operator("object.modifier_add", icon= 'MODIFIER')
       
 
 
 
 
 
class WM_OT_myOp(bpy.types.Operator):
    """Open the Add Cube Dialog box"""
    bl_label = "Add Cube Dialog Box"
    bl_idname = "wm.myop"
   
    text = bpy.props.StringProperty(name= "Enter Name", default= "")
    scale = bpy.props.FloatVectorProperty(name= "Scale:", default= (1,1,1))
   
   
   
    def execute(self, context):
       
        t = self.text
        s = self.scale
       
        bpy.ops.mesh.primitive_cube_add()
        obj = bpy.context.object
        obj.name = t
        obj.scale[0] = s[0]
        obj.scale[1] = s[1]
        obj.scale[2] = s[2]
       
       
        return {'FINISHED'}
   
    def invoke(self, context, event):
       
        return context.window_manager.invoke_props_dialog(self)
 
 
 
 
 
 
       
       
    #Here we are Registering the Classes        
def register():
    bpy.utils.register_class(MainPanel)
    bpy.utils.register_class(PanelA)
    bpy.utils.register_class(PanelB)
    bpy.utils.register_class(WM_OT_myOp)
   
   
 
    #Here we are UnRegistering the Classes    
def unregister():
    bpy.utils.unregister_class(MainPanel)
    bpy.utils.unregister_class(PanelA)
    bpy.utils.unregister_class(PanelB)
    bpy.utils.unregister_class(WM_OT_myOp)
   
    #This is required in order for the script to run in the text editor    
if __name__ == "__main__":
    register()