# https://blender.stackexchange.com/q/57306/3710
# https://blender.stackexchange.com/q/79779/3710

#
# modified for blender 2.80 
# last modification: 2019-09-12 -- add custom-preferences panel -- Emanuel Rumpf --

bl_info = {
    "name": "Add-on Template",
    "description": "",
    "author": "",
    "version": (0, 0, 2),
    "blender": (2, 80, 0),
    "location": "3D View > Tools",
    "warning": "", # used for warning icon and text in addons panel
    "wiki_url": "",
    "tracker_url": "",
    "category": "Development"
}

"""
This is an addon - template for blender 2.80 
Use it as base for new addons.
--
Some changes made for blender 2.80 version (from 2.79):
- Properties are annotations now, assigned with : not =
- bl_region_type now is "UI" not "TOOLS"
- Registration procedure changed: 
  Use bpy.utils.register_class() not register_module()

More information see: python api blender 2.80
"""

import bpy

#import collections
#import importlib

#import mathutils
#import math


from bpy.utils import ( register_class, unregister_class )
from bpy.props import ( StringProperty,
                        BoolProperty,
                        IntProperty,
                        FloatProperty,
                        FloatVectorProperty,
                        EnumProperty,
                        PointerProperty,
                       )
from bpy.types import ( Panel,
                        AddonPreferences,
                        Operator,
                        PropertyGroup,
                      )



# this must match the addon name, use '__package__'
# when defining this in a submodule of a python package.
addon_name = __name__      # when single file 
#addon_name = __package__   # when file in package 


# ------------------------------------------------------------------------
#   settings in addon-preferences panel 
# ------------------------------------------------------------------------


# panel update function for PREFS_PT_MyPrefs panel 
def _update_panel_fnc (self, context):
    #
    # load addon custom-preferences 
    print( addon_name, ': update pref.panel function called' )
    #
    main_panel =  OBJECT_PT_my_panel
    #
    main_panel .bl_category = context .preferences.addons[addon_name] .preferences.tab_label
    # re-register for update 
    unregister_class( main_panel )
    register_class( main_panel )


class PREFS_PT_MyPrefs( AddonPreferences ):
    ''' Custom Addon Preferences Panel - in addon activation panel -
    menu / edit / preferences / add-ons  
    '''

    bl_idname = addon_name

    tab_label: StringProperty(
            name="Tab Label",
            description="Choose a label-name for the panel tab",
            default="New Addon",
            update=_update_panel_fnc
    )

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        col = row.column()
        col.label(text="Tab Label:")
        col.prop(self, "tab_label", text="")





# ------------------------------------------------------------------------
#   properties visible in the addon-panel 
# ------------------------------------------------------------------------

class PG_MyProperties (PropertyGroup):

    my_bool : BoolProperty(
        name="Enable or Disable",
        description="A bool property",
        default = False
        )

    my_int : IntProperty(
        name = "Int Value",
        description="A integer property",
        default = 23,
        min = 10,
        max = 100
        )

    my_float : FloatProperty(
        name = "Float Value",
        description = "A float property",
        default = 23.7,
        min = 0.01,
        max = 30.0
        )

    my_float_vector : FloatVectorProperty(
        name = "Float Vector Value",
        description="Something",
        default=(0.0, 0.0, 0.0), 
        min= 0.0, # float
        max = 0.1
    ) 

    my_string : StringProperty(
        name="User Input",
        description=":",
        default="",
        maxlen=1024,
        )

    my_enum : EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('OP1', "Option 1", ""),
                ('OP2', "Option 2", ""),
                ('OP3', "Option 3", ""),
               ]
        )

# ------------------------------------------------------------------------
#   operators
# ------------------------------------------------------------------------

class OT_HelloWorldOperator (bpy.types.Operator):
    bl_idname = "wm.hello_world"
    bl_label = "Print Values Operator"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool  # this get other class propty

        # print the values to the console
        print("Hello World")
        print("bool state:", mytool.my_bool)
        print("int value:", mytool.my_int)
        print("float value:", mytool.my_float)
        print("string value:", mytool.my_string)
        print("enum state:", mytool.my_enum)

        return {'FINISHED'}

# ------------------------------------------------------------------------
#   menus
# ------------------------------------------------------------------------

class MT_BasicMenu (bpy.types.Menu):
    bl_idname = "OBJECT_MT_select_test"
    bl_label = "Select"

    def draw(self, context):
        layout = self.layout

        # built-in example operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")


# ------------------------------------------------------------------------
#   addon - panel -- visible in objectmode
# ------------------------------------------------------------------------

class OBJECT_PT_my_panel (Panel):
    bl_idname = "OBJECT_PT_my_panel"
    bl_label = "My Panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tool"  # note: replaced by preferences-setting in register function 
    bl_context = "objectmode"   


#   def __init(self):
#       super( self, Panel ).__init__()
#       bl_category = bpy.context.preferences.addons[__name__].preferences.category 

    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop( mytool, "my_bool")
        layout.prop( mytool, "my_enum", text="") 
        layout.prop( mytool, "my_int")
        layout.prop( mytool, "my_float")
        layout.prop( mytool, "my_float_vector", text="")
        layout.prop( mytool, "my_string")
        layout.operator( "wm.hello_world")
        layout.menu( "OBJECT_MT_select_test", text="Presets", icon="SCENE")





# ------------------------------------------------------------------------
# register and unregister
# ------------------------------------------------------------------------

classes = (
    PG_MyProperties,
    #
    OT_HelloWorldOperator,
    MT_BasicMenu,
    OBJECT_PT_my_panel, 
    #
    PREFS_PT_MyPrefs, 
)

def register():
    #
    for cls in classes:
        register_class(cls)
    #
    bpy.types.Scene.my_tool = PointerProperty(type=PG_MyProperties)

    #

def unregister():
    #
    for cls in reversed(classes):
        unregister_class(cls)
    #
    del bpy.types.Scene.my_tool  # remove PG_MyProperties 




if __name__ == "__main__":
    register()