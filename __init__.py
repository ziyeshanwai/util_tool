bl_info = {
    "name": "Example Addon Preferences",
    "author": "Your Name Here",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "Edit > Preferences > Add-ons > Example Addon Preferences",
    "description": "Example Addon",
    "category": "Object",
}

import bpy
import subprocess
import sys
from bpy.types import AddonPreferences
from bpy.props import BoolProperty
from bpy.types import Operator

class InstallOpenCVOperator(Operator):
    bl_idname = "install_opencv.operator"
    bl_label = "安装OpenCV"

    def execute(self, context):
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python"])
            self.report({'INFO'}, "OpenCV已成功安装！")
        except Exception as e:
            self.report({'ERROR'}, f"安装OpenCV时出错：{str(e)}")
        return {'FINISHED'}

class OpenCVAddonPreferences(AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator("install_opencv.operator")

def register():
    bpy.utils.register_class(InstallOpenCVOperator)
    bpy.utils.register_class(OpenCVAddonPreferences)

def unregister():
    bpy.utils.unregister_class(OpenCVAddonPreferences)
    bpy.utils.unregister_class(InstallOpenCVOperator)

if __name__ == "__main__":
    register()