import bpy
from mathutils import Matrix

def camera_matrix2blender_camera_data(camera_matrix, camera_ob):
    assert camera_ob.data.sensor_fit != 'HORIZONTAL', "camera sensor fit mode is wrong"
    f_x = camera_matrix[0][0]
    f_y = camera_matrix[1][1]
    c_x = camera_matrix[0][2]
    c_y = camera_matrix[1][2]
    w = bpy.context.scene.render.resolution_x
    h = bpy.context.scene.render.resolution_y
    sensor_width_in_mm = camera_ob.data.sensor_width
    camera_ob.data.shift_x = -(c_x / w - 0.5)
    camera_ob.data.shift_y = (c_y - 0.5 * h) / w
    camera_ob.data.lens = f_x / w * sensor_width_in_mm
    pixel_aspect = f_y / f_x
    bpy.context.scene.render.pixel_aspect_x = 1.0
    bpy.context.scene.render.pixel_aspect_y = pixel_aspect 
    
    
def build_camera_matrix():
    fx = 849.82
    cx = 498.78
    fy = 848.3
    cy = 498.78
    camera_matrix = Matrix(((fx, 0, cx),(0, fy, cy),(0, 0, 1)))
    return camera_matrix

if __name__ == "__main__":
    camera_matrix = build_camera_matrix()
    camera_ob = bpy.data.objects["Camera"]
    camera_matrix2blender_camera_data(camera_matrix, camera_ob)