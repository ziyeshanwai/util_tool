import bpy


def get_all_rig_gui_names():
    rig_boards = bpy.data.collections["RIGGUI"]
    for ob in rig_boards.all_objects:
        if "CTRL_" in ob.name:
            continue
        else:
            ob.hide_select = True 


if __name__ == "__main__":
    bpy.context.scene.transform_orientation_slots[0].type = 'LOCAL'
    bpy.context.space_data.show_restrict_column_select = True
    get_all_rig_gui_names()