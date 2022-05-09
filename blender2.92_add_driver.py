# https://blender.stackexchange.com/questions/39127/how-to-put-together-a-driver-with-python
# https://blender.stackexchange.com/questions/58886/how-can-i-modify-drivers-properties-via-python-in-blender
import bpy
import os


def add_driver(
        source, target, prop, dataPath,
        index = -1, negative = False, func = ''
    ):
    ''' Add driver to source prop (at index), driven by target dataPath '''

    if index != -1:
        d = source.driver_add( prop, index ).driver
    else:
        d = source.driver_add( prop ).driver

    v = d.variables.new()
    v.name                 = prop
    v.targets[0].id        = target
    v.targets[0].data_path = dataPath

    d.expression = func + "(" + v.name + ")" if func else v.name
    d.expression = d.expression if not negative else "-1 * " + d.expression


def create_driver(ob, data_path, expression):
    mesh = obj.data
    data_path = "key_blocks[\"psd_259\"].value"
    dr = mesh.shape_keys.driver_add(data_path).driver
    dr.type='SCRIPTED'
    dr.expression = expression
    return dr

def add_variable(driver, name, data_path): 
    v = driver.variables.new()
    v.name                 = name
    v.type = 'SINGLE_PROP'
    v.targets[0].id_type = "KEY" # https://docs.blender.org/api/current/bpy.types.DriverTarget.html#bpy.types.DriverTarget
    v.targets[0].id       = bpy.data.shape_keys["Key"]
    v.targets[0].data_path = data_path 
    
if __name__ == "__main__":
    
    obj  = bpy.context.scene.objects['Neutral']
    empty = bpy.context.scene.objects['Empty']
    data_path = "key_blocks[\"psd_259\"].value"
    expression = " browRaiseOuterL * browRaiseInL"
    driver = create_driver(obj, data_path, expression)
    add_variable(driver, "browRaiseOuterL", "key_blocks[\"browRaiseOuterL\"].value")
    add_variable(driver, "browRaiseInL", "key_blocks[\"browRaiseInL\"].value")
