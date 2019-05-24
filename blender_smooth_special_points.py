import bpy
import os
import pickle

def load_index(file):
    with open(file, "rb") as f:
        ind = pickle.load(f)
    return ind

def write_index(file, con):
    with open(file, "wb") as f:
        pickle.dump(con, f)
        
root_path = "\\\\192.168.80.195\\data3\\LiyouWang\\smoothObjs"
file = os.path.join(root_path,"smooth-index.pkl")

#bpy.ops.object.mode_set(mode = 'OBJECT')
#selected_verts = [v for v in bpy.context.active_object.data.vertices if v.select]
#ind = []
#for sv in selected_verts:
#    ind.append(sv.index)
#print(len(ind))
#write_index(file, ind)
ind = load_index(file)

file_names = os.listdir(root_path)
for file in file_names:
    if file.endwith(".obj"):
        bpy.ops.import_scene.obj(filepath=os.path.join(root_path, file))
        bpy.context.scene.objects.active = bpy.context.selected_objects[0]
        obj = bpy.context.active_object
        bpy.ops.object.mode_set(mode = 'EDIT') 
        bpy.ops.mesh.select_mode(type="VERT")
        bpy.ops.mesh.select_all(action = 'DESELECT')
        bpy.ops.object.mode_set(mode = 'OBJECT')
        for i in ind:
            obj.data.vertices[i].select = True
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.vertices_smooth(repeat=5)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.export_scene.obj(filepath=os.path.join(output_path, obj), use_selection=True, use_materials=False)
        bpy.ops.object.delete()
