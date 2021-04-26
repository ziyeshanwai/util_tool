import bpy  
import mathutils
import os


if __name__ == "__main__":
    bs_path = r""
    delta_x = 20
    delta_z = 32
    filenames = os.listdir(bs_path)
    x = 0
    z = 0
    row = 0
    col = 0
    for file in filenames:
        if file.endswith(".obj"):
            x = delta_x * col
            z = delta_z * row
            bpy.ops.import_scene.obj(filepath=os.path.join(bs_path, file), use_split_objects=False,split_mode='OFF')
            bpy.context.selected_objects[0].name = file[:-4]
            bpy.context.selected_objects[0].location = mathutils.Vector((x, 0, z))
            col += 1
            if col>20:
                col = 0
                row += 1
                x = 0