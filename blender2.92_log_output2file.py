import bpy
import numpy as np
import os
import sys

"""
https://blender.stackexchange.com/questions/6921/how-to-write-the-output-of-blender-console-out-to-a-file
"""

if __name__ == "__main__":
    file_path = os.path.join(r"Z:\4Real\Personal\liyouwang\blender_bones_demo", "log.log")
    file = open(file_path, "w")
    sys.stdout = file
    print("test")
    
    bermice_armature = bpy.data.objects["bermice"]
    valerie_armature = bpy.data.objects["valerie"]
    parent_bone_names = ["DHIhead:FACIAL_L_ForeheadMid", "DHIhead:FACIAL_C_LowerLipRotation", "DHIhead:FACIAL_L_EyesackUpper", "DHIhead:FACIAL_C_Jaw", "DHIhead:FACIAL_L_CheekOuter", "DHIhead:FACIAL_R_ForeheadIn", "DHIhead:FACIAL_R_EyelidUpperA", "DHIhead:FACIAL_L_EyelidLowerA", "DHIhead:FACIAL_C_MouthUpper", "DHIhead:FACIAL_C_Forehead", "DHIhead:FACIAL_R_ForeheadOut", "DHIhead:FACIAL_L_EyeCornerOuter", "DHIhead:FACIAL_L_EyelidLowerB",
                         "DHIhead:FACIAL_R_NasolabialBulge", "DHIhead:FACIAL_L_EyelidUpperA", "DHIhead:FACIAL_L_NasolabialBulge", "DHIhead:FACIAL_C_Nose", "DHIhead:FACIAL_L_CheekLower", "DHIhead:FACIAL_R_Ear", "DHIhead:FACIAL_L_EyeCornerInner", "DHIhead:FACIAL_R_Eye", "DHIhead:FACIAL_L_ForeheadOut", "DHIhead:FACIAL_R_EyesackUpper", "DHIhead:FACIAL_L_EyelidUpperFurrow", "DHIhead:FACIAL_R_EyelidUpperFurrow", "DHIhead:FACIAL_R_CheekOuter",
                         "DHIhead:FACIAL_R_CheekInner", "DHIhead:FACIAL_R_EyeCornerOuter", "DHIhead:FACIAL_R_EyesackLower", "DHIhead:FACIAL_L_Eye", "DHIhead:FACIAL_R_CheekLower", "DHIhead:FACIAL_L_EyesackLower", "DHIhead:FACIAL_L_ForeheadIn", "DHIhead:FACIAL_R_ForeheadMid", "DHIhead:FACIAL_R_EyeCornerInner", "DHIhead:FACIAL_L_Ear", "DHIhead:FACIAL_L_EyelidUpperB", "DHIhead:FACIAL_R_EyelidLowerB", "DHIhead:FACIAL_L_CheekInner", "DHIhead:FACIAL_R_EyelidLowerA",
                         "DHIhead:FACIAL_R_EyelidUpperB"]
    middle_level_bone_names = ["DHIhead:FACIAL_C_MouthLower", "DHIhead:FACIAL_R_EyelidUpperA1", "DHIhead:FACIAL_R_EyelidUpperA3", "DHIhead:FACIAL_R_EyelidUpperA2", "DHIhead:FACIAL_L_LipUpper", "DHIhead:FACIAL_C_LipUpper", "DHIhead:FACIAL_L_LipCorner", "DHIhead:FACIAL_R_LipUpperOuter", "DHIhead:FACIAL_R_LipUpper", "DHIhead:FACIAL_L_LipUpperOuter", "DHIhead:FACIAL_R_LipCorner", "DHIhead:FACIAL_L_EyeCornerOuter1", "DHIhead:FACIAL_L_EyelidUpperA3",
                              "DHIhead:FACIAL_L_EyelidUpperA2", "DHIhead:FACIAL_L_EyelidUpperA1", "DHIhead:FACIAL_R_Nostril", "DHIhead:FACIAL_C_NoseTip", "DHIhead:FACIAL_C_NoseLower", "DHIhead:FACIAL_L_Nostril", "DHIhead:FACIAL_R_EyeParallel", "DHIhead:FACIAL_R_EyeCornerOuter1", "DHIhead:FACIAL_L_EyeParallel"]
    all_bone_names = [bone.name for bone in bermice_armature.pose.bones]
    not_inlude_name = all_bone_names[0:6]
    low_level_bone_names = list(set(all_bone_names) - set(not_inlude_name) - set(parent_bone_names) - set(middle_level_bone_names))
    bone_names = parent_bone_names
    bpy.context.scene.frame_current = 1
    bpy.context.view_layer.update()
    bermice_bone_rest_location = []
    bermice_bone_rest_rotation = []
    valerie_bone_rest_location = []
    valerie_bone_rest_rotation = []
    bone_names = all_bone_names[6:]
    print("the length of bone names is {}".format(len(bone_names)))
    for bone in bone_names:
        location = bermice_armature.pose.bones[bone].location[0:3]
        bermice_bone_rest_location.append(list(location))
        rotation = bermice_armature.pose.bones[bone].rotation_quaternion.to_euler()[0:3]
        bermice_bone_rest_rotation.append(list(rotation))
        location = valerie_armature.pose.bones[bone].location[0:3]
        valerie_bone_rest_location.append(list(location))
        rotation = valerie_armature.pose.bones[bone].rotation_quaternion.to_euler()[0:3]
        valerie_bone_rest_rotation.append(list(rotation)) 
    bermice_bone_rest_location_np = np.array(bermice_bone_rest_location)
    bermice_bone_rest_rotation_np = np.array(bermice_bone_rest_rotation)
    valerie_bone_rest_location_np = np.array(valerie_bone_rest_location)
    valerie_bone_rest_rotation_np = np.array(valerie_bone_rest_rotation)
    for i in range(0, 230):
        bpy.context.scene.frame_current = i
        bpy.context.view_layer.update() 
        bermice_bone_location = []
        bermice_bone_rotation = []
        valerie_bone_location = []
        valerie_bone_rotation = []
        for bone in bone_names:
            location = bermice_armature.pose.bones[bone].location[0:3]
            bermice_bone_location.append(list(location))
            rotation = bermice_armature.pose.bones[bone].rotation_quaternion.to_euler()[0:3]
            bermice_bone_rotation.append(list(rotation))
            location = valerie_armature.pose.bones[bone].location[0:3]
            valerie_bone_location.append(list(location))
            rotation = valerie_armature.pose.bones[bone].rotation_quaternion.to_euler()[0:3]
            valerie_bone_rotation.append(list(rotation))
        bermice_bone_location_np = np.array(bermice_bone_location)
        print("frame:{} ".format(i))
        print("bermice location {}".format(np.where(np.linalg.norm(bermice_bone_location_np-bermice_bone_rest_location_np, axis=1)>0)[0]))
        bermice_bone_rotation_np = np.array(bermice_bone_rotation)
        print("bermice rotation {}".format(np.where(np.linalg.norm(bermice_bone_rotation_np-bermice_bone_rest_rotation_np, axis=1)>0)[0]))
        valerie_bone_location_np = np.array(valerie_bone_location)
        print("valerie location {}".format(np.where(np.linalg.norm(valerie_bone_location_np-valerie_bone_rest_location_np, axis=1)>0)[0]))
        valerie_bone_rotation_np = np.array(valerie_bone_rotation)
        print("valerie rotation {}".format(np.where(np.linalg.norm(valerie_bone_rotation_np-valerie_bone_rest_rotation_np, axis=1)>0)[0]))
#        print("frame:{}, location err:{}, rotation err:{}".format(i, np.linalg.norm(bermice_bone_location_np - valerie_bone_location_np, axis=1).mean(),np.linalg.norm(bermice_bone_rotation_np - valerie_bone_rotation_np, axis=1).mean()))
#        print("frame:{}, location err:{}, rotation err:{}".format(i, np.linalg.norm(bermice_bone_location_np - bermice_bone_rest_location_np, axis=1).mean(),np.linalg.norm(bermice_bone_rotation_np - bermice_bone_rest_rotation_np, axis=1).mean()))
    sys.stdout = sys.__stdout__ #reset
    file.close()