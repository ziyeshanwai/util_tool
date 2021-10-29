import bpy
import os

ob = bpy.data.objects["ob_name"]
output_path = r"path" 
for key_block in ob.data.shape_keys.key_blocks:
    key_block.value = 1
    bpy.ops.export_scene.obj(filepath=os.path.join(output_path, "{}.obj".format(key_block.name)), use_selection=True, use_mesh_modifiers=True, use_uvs=False, use_materials=False)
    key_block.value = 0