import bpy
      
       
def set_scale_nodes_selected_objects(scale_val):
    for obj in bpy.context.selected_objects:
        for mat_slot in obj.material_slots:
            set_scale_nodes_material(mat_slot.material, scale_val)
    

def set_scale_nodes_material(mat, scale_val):
    if mat is not None and mat.use_nodes and mat.node_tree is not None:
        for node in mat.node_tree.nodes:
            if node.label == "head_wm1_normal_head_wm1_browsRaiseInner_L" and node.type == "VALUE":
                node.outputs["Value"].default_value = scale_val  


if __name__ == "__main__":
    scale_val = 1.0
    set_scale_nodes_selected_objects(scale_val)
