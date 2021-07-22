import cv2
import numpy as np
import bpy
import pickle
import os
import math
from scipy.spatial.transform import Rotation as R


def LoadXML(file_name, node_name):
    """
    :param file_name: 读取的xml文件的路径和名称
    :param node_name: 读取的xml文件的节点名字
    :return: 返回对应节点名称的内容
    """
    # just like before we specify an enum flag, but this time it is
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(file_name, cv2.FILE_STORAGE_READ)
    # for some reason __getattr__ doesn't work for FileStorage object in python
    # however in the C++ documentation, getNode, which is also available,
    # does the same thing
    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    matrix = cv_file.getNode(node_name).mat()
    cv_file.release()
    return matrix


def ini_data(camera_name, camera_matrix):
    
    fx = camera_matrix[1][1]
    fy = camera_matrix[0][0]
    cx = camera_matrix[1][2]
    cy = camera_matrix[0][2]
    camera_ob = bpy.data.objects[camera_name]
    w = bpy.context.scene.render.resolution_x
    h = bpy.context.scene.render.resolution_y
    cameraMatrix = np.array([[fx, 0, cx],[0, fy, cy],[0, 0, 1]], dtype=np.float32)
    distCoeffs = np.array([0, 0, 0, 0, 0], dtype = np.float32)
    assert camera_ob.data.sensor_fit == 'HORIZONTAL', "camera sensor fit mode is wrong"
    sensor_width_in_mm = camera_ob.data.sensor_width
    camera_ob.data.shift_x = -(cx / w - 0.5)
    camera_ob.data.shift_y = (cy - 0.5 * h) / w
    camera_ob.data.lens = fx / w * sensor_width_in_mm
    pixel_aspect = fy / fx
    bpy.context.scene.render.pixel_aspect_x = 1.0
    bpy.context.scene.render.pixel_aspect_y = pixel_aspect 
    bpy.context.view_layer.update()
    return cameraMatrix, distCoeffs

# Checks if a matrix is a valid rotation matrix.
def isRotationMatrix(R) :
    Rt = np.transpose(R)
    shouldBeIdentity = np.dot(Rt, R)
    I = np.identity(3, dtype = R.dtype)
    n = np.linalg.norm(I - shouldBeIdentity)
    return n < 1e-6

# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :

    assert(isRotationMatrix(R))

    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])

    singular = sy < 1e-6

    if not singular :
        x = math.atan2(-R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(-R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0

    return np.array([x, y, z])

def R2qua(R_ma):
    r = R.from_matrix(R_ma)
    print(r.as_euler('xyz', degrees=True))
    qua = r.as_quat()
    return qua


def build_camera_matrix_buildin(Camera_name):
    # get the relevant data
    cam = bpy.data.objects[Camera_name].data
    scene = bpy.context.scene
    # assume image is not scaled
    assert scene.render.resolution_percentage == 100
    # assume angles describe the horizontal field of view
    assert cam.sensor_fit != 'VERTICAL'

    f_in_mm = cam.lens
    sensor_width_in_mm = cam.sensor_width

    w = scene.render.resolution_x
    h = scene.render.resolution_y

    pixel_aspect = scene.render.pixel_aspect_y / scene.render.pixel_aspect_x

    f_x = f_in_mm / sensor_width_in_mm * w
    f_y = f_x * pixel_aspect

    # yes, shift_x is inverted. WTF blender?
    c_x = w * (0.5 - cam.shift_x)
    # and shift_y is still a percentage of width..
    c_y = h * 0.5 + w * cam.shift_y

    cameraMatrix = np.array([[f_x, 0, c_x], [0, f_y, c_y], [0,   0,   1]])
    
    distCoeffs = np.array([0, 0, 0, 0, 0], dtype = np.float32)
    return cameraMatrix, distCoeffs


def get_faceindex(faceindex_path):
    face_index = load_pickle_file(faceindex_path)
    return np.array(face_index)


def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))

def myR2euler(R):
    roll = math.atan2(-R[2][1], R[2][2])
    pitch = math.asin(R[2][0])
    yaw = math.atan2(-R[1][0], R[0][0])
    return np.array([roll, pitch, yaw])

def get_camera_positon_rotation(objectPoints, imagePoints, cameraMatrix, distCoeffs, Camera_names):
    R_bcam2cv = np.array([[1, 0,  0], [0, -1, 0],[0, 0, -1]])
    _, rVec, tVec = cv2.solvePnP(objectPoints, imagePoints, cameraMatrix, distCoeffs)
    rmat, _ = cv2.Rodrigues(rVec)
    R = rmat.transpose()
    pos = -R @ tVec
#    pos = R_bcam2cv.dot(pos)
    pos = pos.flatten()
    bpy.data.objects[Camera_names].location[0] = pos[0]
    bpy.data.objects[Camera_names].location[1] = pos[1]
    bpy.data.objects[Camera_names].location[2] = pos[2]
    R = R_bcam2cv.dot(R)  # import tant !
    use_qua = True
    if use_qua:
        qua = R2qua(R)
        bpy.data.objects[Camera_names].rotation_quaternion[0]=qua[3]
        bpy.data.objects[Camera_names].rotation_quaternion[1]=qua[0]
        bpy.data.objects[Camera_names].rotation_quaternion[2]=qua[1]
        bpy.data.objects[Camera_names].rotation_quaternion[3]=qua[2]
        
    else:
        
#        euler_angle = rotationMatrixToEulerAngles(R)
        euler_angle = myR2euler(R)
        bpy.data.objects[Camera_names].rotation_euler[0]=euler_angle[0]
        bpy.data.objects[Camera_names].rotation_euler[1]=euler_angle[1]
        bpy.data.objects[Camera_names].rotation_euler[2]=euler_angle[2]
    bpy.context.view_layer.update()

def get_marker_position(clip_name, frame):
    """
    get frame coordinate in pixle
    """
    track_data = bpy.data.movieclips[clip_name].tracking
    clip_width = bpy.data.movieclips[clip_name].size[0]
    clip_height = bpy.data.movieclips[clip_name].size[1]
    pix_coor = []
    ind = []
    coor_arr = []
    for t in track_data.tracks:
        x = t.markers.find_frame(frame).co.xy[0] * clip_width
        y = (1 - t.markers.find_frame(frame).co.xy[1]) * clip_height
        pix_coor.append({t.name:(x, y)})
        coor_arr.append([x, y])
        ind.append(int(t.name))
#    print("marker position is {}".format(pix_coor))
    return np.array(coor_arr), ind


def get_obj_coodinate(ob, face_index):
    coor_list = []
    for ind in face_index:
        coor = ob.matrix_world @ ob.data.vertices[ind].co  # cannot invered
        coor_list.append([coor[0], coor[1], coor[2]])
    return np.array(coor_list)


def mark_op():
    """
    no use
    """
    for i in range(10):
        # this adds a new point to be tracked
        trck = track_data.tracks.new()
        for f in range(1,100,10):
            # this sets the location of the point at frame f
            x = (f+i) * 0.1
            y = (f+i) * 0.1
            trck.markers.insert_frame(f, co=(x,y))
    for m in t.markers:
        print(t.name)
        print('marker on frame {} at {}'.format(m.frame, m.co))
    


if __name__ == "__main__":
    """
    使用旋转矩阵转化为四元数计算出来的旋转在blender内有问题，需要手工调解下旋转信息
    """
    clip_name = 'xxx.mp4'
    ob = bpy.data.objects['xxx']
    imagePoints_1, ind_1 = get_marker_position(clip_name, 0)
    face_ind_path = os.path.join(r"xxx", "xxx")
    face_ind = get_faceindex(face_ind_path)
    marker_3d_index_1 = face_ind[ind_1]
    objectPoints_1 = get_obj_coodinate(ob, marker_3d_index_1)
    camera_name = 'Camera1'
    camera_matrix = LoadXML(os.path.join(r"xxxx", "xxx.xml"), "camera_matrix")
    print("camera matrix is {}".format(camera_matrix))
    cameraMatrix, distCoeffs = ini_data(camera_name, camera_matrix)
#    cameraMatrix, distCoeffs = build_camera_matrix_buildin(camera_name)
    print(cameraMatrix)
    get_camera_positon_rotation(objectPoints_1, imagePoints_1, cameraMatrix, distCoeffs, camera_name)
#    
    clip_name = 'xxx.mp4'
    imagePoints_2, ind_2 = get_marker_position(clip_name, 0)
    marker_3d_index_2 = face_ind[ind_2]
    objectPoints_2 = get_obj_coodinate(ob, marker_3d_index_2)
    camera_name = 'Camera2'
    camera_matrix = LoadXML(os.path.join(r"xxxx", "xxx.xml"), "camera_matrix")
    cameraMatrix, distCoeffs = ini_data(camera_name, camera_matrix)
#    cameraMatrix, distCoeffs = build_camera_matrix_buildin(camera_name)
    print(cameraMatrix)
    get_camera_positon_rotation(objectPoints_2, imagePoints_2, cameraMatrix, distCoeffs, camera_name)