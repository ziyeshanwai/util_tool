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
        
        
        
if __name__ == '__main__':
    eye_weights_path = r"\\192.168.20.63\ai\Liyou_wang_data\test_data\bs_eyeball.pkl"
    weights = load_pickle_file(eye_weights_path)
    for i in range(0, len(weights)):
        up, down, left, right = weights[i]
        bpy.data.objects['left_eye'].rotation_euler[0] = (-25*up + 25*down)/180 * 3.14 # up down
        bpy.data.objects['left_eye'].rotation_euler[1] = 0
        bpy.data.objects['left_eye'].rotation_euler[2] = (-30*up + 30*down)/180 * 3.14
        bpy.data.objects['left_eye'].keyframe_insert(data_path="rotation_euler", frame=i)
        bpy.data.objects['right_eye'].rotation_euler[0] = (-25*up + 25*down)/180 * 3.14 # up down
        bpy.data.objects['right_eye'].rotation_euler[1] = 0
        bpy.data.objects['right_eye'].rotation_euler[2] = (-30*up + 30*down)/180 * 3.14
        bpy.data.objects['right_eye'].keyframe_insert(data_path="rotation_euler", frame=i)
        #bpy.context.active_object.rotation_euler[0] = (-25*up + 25*down)/180 * 3.14 # up down
        #bpy.context.active_object.rotation_euler[1] = 0
        #bpy.context.active_object.rotation_euler[2] =  (-30*up + 30*down)/180 * 3.14
        #bpy.context.active_object.keyframe_insert(data_path="rotation_euler", frame=i)