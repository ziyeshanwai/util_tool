import bpy
import os
import pickle

def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))


if __name__ == "__main__":
    output_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\xiaoyueblendshapes"
    names = ["Basis","L_cheekSquint", "R_mouthStretchDn_Fix", "L_browOut_Up", "cheekShrink","L_noseOut","R_eyeBlink_Up","R_browOut_Up","jawUp","mouth_F","L_nose","mouth_Dn","L_mouthStretchDn_Fix","L_mouthSmile","mouthSad","R_browIn_Dn", "jawOpen", "L_eyeBlink_Up", "R_eyeSquint", "R_eyeLook", "R_cheekSquint", "L_browIn_Up", "mouthPucker", "L_browIn", "R_mouth_Dn", "R_jaw", "brow_Dn", "L_mouthStretch", "mouth_O", "L_mouth_Up", "R_noseIn", "browIn_Up", "mouth_Up", "R_nose", "L_mouth_Dn", "browIn_Fix", "R_browIn_Up", "L_mouthUp", "mouthRoll"]
    for i in range(0, 39):
        bpy.context.object.active_shape_key_index = i
        if i > 0:
            bpy.data.shape_keys["Key"].key_blocks[names[i]].value = 1
        bpy.ops.export_scene.obj(filepath=os.path.join(output_path, "{}.obj".format(names[i])), use_selection=True, use_mesh_modifiers=True, use_uvs=False, use_materials=False)
        bpy.data.shape_keys["Key"].key_blocks[names[i]].value = 0
    save_pickle_file(os.path.join(output_path, "names.pkl"), names)