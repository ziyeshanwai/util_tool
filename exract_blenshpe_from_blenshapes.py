import bpy
import os


if __name__ == "__main__":
    output_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\xiaoyueblendshapes"
    names = ["Basis","eyeLook_Dn", "R_eyeSquint", "mouthRoll", "L_mouthStretch","L_nose","R_eyeBlink_Up","L_mouth","R_jaw","browIn_Up","L_mouthFunnel","R_mouthUp","R_mouth","L_mouth_Up","jawUp","L_browIn_Up", "R_mouth_Dn", "R_mouthSad", "L_eyeBlink_Up", "L_brow_Up", "L_mouthUp", "mouthSad", "R_browIn_Up", "brow_Up", "mouth_Up", "jawOpen", "mouth_Dn", "L_mouthSmile", "L_mouth_Dn", "L_eyeLook", "R_mouthStretch", "L_jaw", "L_eyeSquint", "R_mouthFunnel", "R_cheekSquint", "R_eyeWide", "cheekShrink", "R_nose", "mouth_OO"]
    for i in range(0, 39):
        bpy.context.object.active_shape_key_index = i
        if i > 0:
            bpy.data.shape_keys["Key.001"].key_blocks[names[i]].value = 1
        bpy.ops.export_scene.obj(filepath=os.path.join(output_path, "{}.obj".format(names[i])), use_selection=True, use_mesh_modifiers=True, use_uvs=False, use_materials=False)
        bpy.data.shape_keys["Key.001"].key_blocks[names[i]].value = 0