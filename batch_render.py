
import bpy
import os
import glob
import sys

"""
console render batch 
https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html
"""

for window in bpy.context.window_manager.windows:
    screen = window.screen

for area in screen.areas:
    if area.type == 'VIEW_3D':
        override = {'window': window, 'screen': screen, 'area': area}
        bpy.ops.screen.screen_full_area(override)
        break


def load_obj(objfile):
    print("name is {}".format(objfile))
    bpy.ops.import_scene.obj(filepath=objfile)
    bpy.context.selected_objects[0].name = "tmp"
    bpy.ops.object.shade_smooth()
    return "tmp"


def set_mat(obname, tex_name):
    """
    https://blender.stackexchange.com/questions/157531/blender-2-8-python-add-texture-image
    """
    mat = bpy.data.materials.new(name="MAT")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    texImage = mat.node_tree.nodes.new('ShaderNodeTexImage')
    texImage.image = bpy.data.images.load(tex_name)
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
    mat.node_tree.links.new(bsdf.inputs['Base Color'], texImage.outputs['Color'])
    bsdf.inputs[4].default_value = 0.178
    bsdf.inputs[7].default_value = 0.459
    ob = bpy.data.objects[obname]

    # Assign it to object
    if ob.data.materials:
        ob.data.materials[0] = mat
    else:
        ob.data.materials.append(mat)
        

def delete_data():
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects['tmp'].select_set(True)
    bpy.ops.object.delete()
    
    for mesh in bpy.data.meshes:
        if mesh.users == 0:
            bpy.data.meshes.remove(mesh)
    for mat in bpy.data.materials:
        if mat.users == 0:
            bpy.data.materials.remove(mat)
    for img in bpy.data.images:
        if img.users == 0:
            bpy.data.images.remove(img)


def renderandsave(name):
    bpy.context.scene.render.filepath = "{}.png".format(name)
    bpy.ops.render.render(use_viewport = True, write_still=True)            

            
def main():
    argv = sys.argv
    print("argv is {}".format(argv))
    obj_path = argv[argv.index("-op") + 1]
    texture_path = argv[argv.index("-tp") + 1]
    render_out = argv[argv.index("-rp") + 1]
    print("obj_path is {}".format(obj_path))
    print("texture_path is {}".format(texture_path))
    print("render_out is {}".format(render_out))
    objs = sorted(glob.glob(os.path.join(obj_path, "*.obj")))
    textures = sorted(glob.glob(os.path.join(texture_path, "*.png")))
    for i in range(0, len(objs)):
        print("load {}, {}".format(objs[i], textures[i]))
        load_obj(objs[i])
        set_mat("tmp", textures[i])
        renderandsave(os.path.join(render_out, "render_{:0>4d}".format(i)))
        delete_data()
    


if __name__ == "__main__":
    main()