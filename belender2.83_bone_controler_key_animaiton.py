import bpy
import os
import pickle

def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))
        
        
if __name__ == "__main__":
    weight_list_path = os.path.join(r"path", "weights_eye_list.pkl")
    eye_left_right_limimit = [-0.048, 0.048]
    eye_up_down_limit = [-0.022, 0.022]
    eye_l_r_scale = 0.048
    eye_u_d_scale = 0.022
    jaw_open2_bone = 20
    weight = load_pickle_file(weight_list_path)
    for i, w in enumerate(weight):
        bpy.context.object.pose.bones["eye_mian"].location[0] = - w[0] * eye_l_r_scale * 100
        bpy.context.object.pose.bones["eye_mian"].location[1] = w[1] * eye_u_d_scale * 100
        bpy.context.object.pose.bones["eye_mian"].keyframe_insert("location", frame=i)
        if i % 100 == 0:
            print("insert {}".format(i))
            print("location is {}".format( bpy.context.object.pose.bones["eye_mian"].location))
        bpy.context.object.pose.bones["jaw.con"].rotation_euler[0] = bpy.data.objects['head_geo'].data.shape_keys.animation_data.action.fcurves[17].keyframe_points[i].co[1] * 65 / 180
        bpy.context.object.pose.bones["jaw.con"].keyframe_insert("rotation_euler", frame=i)    
    