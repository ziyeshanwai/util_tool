import bpy
import json
import math
import os
from mathutils import Matrix, Euler, Vector


def load_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def create_armature_from_json(json_data):
    # Create a new armature object
    armature = bpy.data.armatures.new('Armature')
    armature_obj = bpy.data.objects.new('Armature', armature)
    bpy.context.collection.objects.link(armature_obj)
    bpy.context.view_layer.objects.active = armature_obj
    #bpy.ops.object.armature_add(enter_editmode=True)
    #armature = bpy.context.object
    #armature.name = "Imported_Armature"
    bpy.ops.object.mode_set(mode='EDIT')
    
    bones_dict = {}
    
    for bone_info in json_data:
        bone_name = bone_info['name']
        parent_name = bone_info['parent']
        position = bone_info['position']
        rotation = bone_info['rotation']
        
        # Create new bone
        bone = armature_obj.data.edit_bones.new(bone_name)
        bone.head = position
        
        rotation_radians = [math.radians(rot) for rot in rotation]
        rotation_matrix = Euler(rotation_radians).to_matrix().to_4x4()
        
        direction = Vector((0.0, 1, 0.0))
        global_direction = rotation_matrix @ direction
        bone.tail = Vector(position) + global_direction
        # Convert rotation from degrees to radians and set orientation
#        bone.tail = [position[0], position[1] + 0.1, position[2]]  # Arbitrary tail, adjusted later if needed
        bone.roll = 0
        
        # Store bone in a dictionary for parenting
        bones_dict[bone_name] = bone
        
        # Set parent
        if parent_name != "None":
            bone.parent = bones_dict[parent_name]
    
    # Finalize the armature
    bpy.ops.object.mode_set(mode='OBJECT')
    
    return armature_obj

def assign_weights_to_mesh(armature, json_data):
    # Assuming the mesh object is already selected
    mesh = bpy.data.objects["f_med_unw_body_lod0_mesh2Shape"]
    bpy.context.view_layer.objects.active = mesh
    bpy.ops.object.modifier_add(type='ARMATURE')
    mesh.modifiers["Armature"].object = armature
    
    for bone_info in json_data:
        bone_name = bone_info['name']
        influences = bone_info['influences']
        
        if influences == "None":
            continue
        
        for mesh_name, vertex_data in influences.items():
            if mesh_name == mesh.name:
                for vtx_info in vertex_data:
                    vtx_index = vtx_info['vertex_index']
                    weight = vtx_info['weight']
                    
                    # Ensure the vertex group exists
                    if bone_name not in mesh.vertex_groups:
                        mesh.vertex_groups.new(name=bone_name)
                    
                    # Assign the weight to the vertex
                    mesh.vertex_groups[bone_name].add([vtx_index], weight, 'REPLACE')

# Example usage
json_file_path = bpy.path.abspath(r"D:\blenderAddonsDevProjects\BODYMODEL\body.json")
json_data = load_json_file(json_file_path)

# Create armature from JSON
armature = create_armature_from_json(json_data)

# Assuming you have a selected mesh, assign weights
assign_weights_to_mesh(armature, json_data)

print("Armature and weights imported successfully.")
