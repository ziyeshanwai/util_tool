import bpy
import os

if __name__ == "__main__":
    obj_path = r"D:\pycharm_projects\BSGECMD\A\frame_4d"
    objs = os.listdir(obj_path)
    i = 0
    j = 0
    for o in objs:
        imported_object = bpy.ops.import_scene.obj(filepath=os.path.join(obj_path, o))
        obj_object = bpy.context.selected_objects[0]
        obj_object.name = o[:-4]
        obj_object.location[0] = 20 * i
        obj_object.location[1] = 25 * j
        if i == 10:
            i = -1
            j += 1
        i += 1
        
