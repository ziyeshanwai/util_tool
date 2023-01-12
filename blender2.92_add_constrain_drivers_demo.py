import bpy

def _rm_active_ob_driver():
    """
    delete shape key driver
    """
    for b in bpy.context.active_object.data.shape_keys.key_blocks:
        b.driver_remove('value')
        
        
def connect_rig_board_and_shapkey():
    pass

def create_driver(ob, data_path, expression):
    mesh = ob.data
    data_path = data_path
    dr = mesh.shape_keys.driver_add(data_path).driver
    dr.type='SCRIPTED'
    dr.expression = expression
    return dr

def add_SINGLE_PROP_variable(driver, name, data_path):
    v = driver.variables.new()
    v.name = name
    v.type = 'SINGLE_PROP'
    v.targets[0].id_type = "KEY" # https://docs.blender.org/api/current/bpy.types.DriverTarget.html#bpy.types.DriverTarget
    v.targets[0].id       = bpy.data.shape_keys["Key"]
    v.targets[0].data_path = data_path
        
def add_transform_variable(driver, name, id): 
    v = driver.variables.new()
    v.name = name
    v.type = 'TRANSFORMS'
    print("ttype is {}".format(v.targets[0].id_type))
    #v.targets[0].id_type = "Object" # https://docs.blender.org/api/current/bpy.types.DriverTarget.html#bpy.types.DriverTarget
    v.targets[0].id       = id
    #v.targets[0].data_path = data_path
    v.targets[0].transform_space = "LOCAL_SPACE" # 
    v.targets[0].transform_type = "LOC_Y"  # enum in [‘LOC_X’, ‘LOC_Y’, ‘LOC_Z’, ‘ROT_X’, ‘ROT_Y’, ‘ROT_Z’, ‘ROT_W’, ‘SCALE_X’, ‘SCALE_Y’, ‘SCALE_Z’, ‘SCALE_AVG’], default ‘LOC_X’

def add_location_constraint(controller_ob):
    con_limit_location = controller_ob.constraints.new(type='LIMIT_LOCATION')
    con_limit_location.use_min_x = True
    con_limit_location.use_min_y = True
    con_limit_location.use_min_z = True
    con_limit_location.use_max_x = True
    con_limit_location.use_max_y = True
    con_limit_location.use_max_z = True
    con_limit_location.min_y = 0.0
    con_limit_location.max_y = 1
    con_limit_location.owner_space="LOCAL"
    


if __name__ == "__main__":
    controller_ob = bpy.data.objects["CTRL_L_brow_down"]
    driver_ob = bpy.data.objects["CTRL_expressions_neutral"]
    #add_location_constraint(controller_ob)
    data_path = "key_blocks[\"CTRL_expressions_browDownL\"].value"
    expression = "CTRL_expressions_browDownL"
    driver = create_driver(driver_ob, data_path, expression)
    add_transform_variable(driver, "CTRL_expressions_browDownL", controller_ob)