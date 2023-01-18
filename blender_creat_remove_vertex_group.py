import bpy



def _creat_vertex_group(ob, group_name, vertex_index):
    """
    https://b3d.interplanety.org/en/how-to-create-a-vertex-group-and-add-vertices-to-it-with-the-blender-python-api/
    """
    new_vertex_group = ob.vertex_groups.new(name=group_name)
    vertex_group_data = vertex_index
    new_vertex_group.add(vertex_group_data, 1.0, 'ADD')

def _remove_all_groups(ob):
    for g in ob.vertex_groups:
        ob.vertex_groups.remove(g)
        
        
if __name__ == "__main__":
    ob = bpy.context.active_object
    _remove_all_groups(ob)