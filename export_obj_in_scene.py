import bpy
import os
import pickle


def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))
        
bpy.ops.object.select_all(action="DESELECT")
output_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\xiaoyueblendshapes"
names = []
for obj in bpy.context.scene.objects:
    obj.select = True
    bpy.ops.export_scene.obj(filepath=os.path.join(output_path, "{}.obj".format(obj.name)), use_selection=True, use_materials=False)
    names.append("{}.obj".format(obj.name))
    bpy.ops.object.delete()
save_pickle_file(os.path.join(output_path, "names.pkl"), names)