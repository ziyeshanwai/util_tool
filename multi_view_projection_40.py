import cv2
import torch
import sys
sys.path.append("./..")
sys.path.append(".")
from manopth.manolayer import ManoLayer
from Util.util import *
import numpy as np
from load_2d_keypoints import GetJsonCorList, get_Cordinate_2d


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


def DumpXML(file_name, matrix, node_name):
    """

    :param file_name: 需要保存的文件名称
    :param matrix: 需要保存的矩阵
    :param node_name: 需要保存的节点名称
    :return: 无
    """
    # notice how its almost exactly the same, imagine cv2 is the namespace for cv
    # in C++, only difference is FILE_STORGE_WRITE is exposed directly in cv2
    cv_file = cv2.FileStorage(file_name, cv2.FILE_STORAGE_WRITE)
    # this corresponds to a key value pair, internally opencv takes your numpy
    # object and transforms it into a matrix just like you would do with <<
    # in c++
    cv_file.write(node_name, matrix)
    # note you *release* you don't close() a FileStorage object
    cv_file.release()


def get_Cordinate(Frames_keypoints, i):
    frame = Frames_keypoints[i]
    Cordinates = []
    confidences = []
    for j in range(0, len(frame), 4):
        Cordinates.append([frame[j], frame[j + 1], frame[j + 2]])
        confidences.append(frame[j+3])
    Cors = np.array(Cordinates, dtype=np.float32)
    confiden = np.array(confidences, dtype=np.float32)
    return Cors, confiden


def Project_to_2d(hand_cor, M):
    """

    :param cors: 根据2D点计算出来的3D手的坐标关键点
    :param hand_cor: Mano的手的关键点坐标
    :param M: 相机内外参矩阵
    :return: 返回uv Mano的手的uv 坐标
    """

    ones = np.ones((21, 1))
    hand_Homo_coor = np.hstack((hand_cor, ones))
    project_point = M.dot(hand_Homo_coor.T)
    uv_cor = (1 / project_point.T[:, 2][:, np.newaxis]) * project_point.T
    return uv_cor


def Project_to_2d_torch(hand_cor, camera_r_t, Intrinsics):
    """

    :param cors: 根据2D点计算出来的3D手的坐标关键点
    :param hand_cor: Mano的手的关键点坐标
    :param M: 相机内外参矩阵
    :return: 返回uv Mano的手的uv 坐标
    """
    ones = torch.ones((21, 1))
    hand_Homo_coor = torch.cat((hand_cor, ones), dim=1)
    project_point = torch.from_numpy(Intrinsics.astype(np.float32)).mm(camera_r_t).mm(hand_Homo_coor.t())

    uv_cor = torch.mul(1 / project_point.t()[:, 2].unsqueeze(1), project_point.t())
    return uv_cor


if __name__ == "__main__":
    hand_output_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\Hand_Data\\output_transform_6"
    file_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\Hand_Data\\camera\\camera_2019_7_5_1"
    Camera_names = ["48070810266", "48070810273", "48072910098", "48072910099", "48072910100", "48072910102",
                    "48072910103", "48072910104", "48072910105", "48072910107", "48072910108", "48072910109",
                    "48072910110", "48072910111", "48072910114", "48170110023", "48170110026", "48170110038",
                    "48170110028", "48170110036", "48170110037", "48170110032", "48170110024", "48170110033",
                    "48170110041", "48182210098", "48182210099", "48182210101", "48182210103", "48182210104",
                    "48182210106", "49011110004", "49011110010", "49011110011", "49011110012", "49011110015",
                    "49011110019", "49011110021", "49011110022", "49011110024"]
    # Camera_names = ["48072910098", "48072910104", "48170110037", "49011110010", "48182210099", "48170110037"]
    # error = ["48170110032", "48170110024", "48170110033","48170110038"]
    node_name_0 = "CameraMatrix"
    node_name_1 = "Intrinsics"
    node_name_2 = "Distortion"
    ncomps = 45
    Camera_number = len(Camera_names)
    mano_layer = ManoLayer(
        mano_root='D:\\pycharm_project\\Fit_hands\\manopth\\mano\\models', use_pca=True, ncomps=ncomps,
        flat_hand_mean=False)
    image = os.path.join("\\\\192.168.20.63\\ai\\Liyou_wang_data\\Hand_Data\\Image\\48072910104", "001.jpeg")
    Camera_matrixs = []
    Intrinsics = []
    for name in Camera_names:
        xml_file = os.path.join(file_path, "{}.xml".format(name))
        came_mat = LoadXML(xml_file, node_name_0)
        Camera_r_t = torch.from_numpy(came_mat.astype(np.float32))
        Camera_r_t.requires_grad = False
        Camera_matrixs.append(Camera_r_t)
        ins = LoadXML(xml_file, node_name_1)
        Intrinsics.append(ins)

    print("load mano torch model... ")
    random_shape = torch.rand(1, 10)
    random_shape.requires_grad = True
    random_pose = torch.rand(1, ncomps + 3)
    random_pose.requires_grad = True
    hand_verts, hand_joints = mano_layer(random_pose, random_shape)
    face = mano_layer.th_faces + 1

    loss_fn = torch.nn.MSELoss(reduce=False, size_average=True)  # (a - b)^2
    learning_rate = 1e-3
    first_time = True
    i = 0
    Hand_joints_list = []
    json_file = os.path.join("\\\\192.168.20.63\\ai\\Liyou_wang_data\\Hand_Data\\json\\2019_07_05_11_06_37_0_1", "3dkeypointsNot.json")
    cor = None
    f = open(json_file, 'r')
    Frames_keypoints = []
    for line in f.readlines():
        dic = json.loads(line)
        cor = dic['people'][0]["hand_right_keypoints_3d"]
        Frames_keypoints.append(cor)
    f.close()
    cors, _ = get_Cordinate(Frames_keypoints, 0)  # 抽取指定帧
    hand_verts, hand_joints = mano_layer(random_pose, random_shape)
    hand_cor = hand_joints[0, :, :]
    hand_cor_aligned, s, R, t = AlignTwoFaceWithFixedPoints(cors, hand_cor.detach().numpy(), [0, 2, 5, 9, 13, 17], non_linear_align=False,
                                                    return_sRt=True)
    s = s.astype(np.float32)
    R = R.astype(np.float32)
    t = t.astype(np.float32)
    key_points_2d_lists = []
    Frame_2d_numbers_list = []
    for name in Camera_names:
        key_points_2d_json_file = os.path.join("\\\\192.168.20.63\\ai\\Liyou_wang_data\\Hand_Data\\json", name, "2dkeypoints.json")
        key_points_2d_list, Frame_numbers = GetJsonCorList(key_points_2d_json_file)
        key_points_2d_lists.append(key_points_2d_list)
        Frame_2d_numbers_list.append(Frame_numbers)
    number_frames = len(Frames_keypoints)
    optimizer = torch.optim.Adam([random_shape, random_pose, Camera_r_t], lr=1e-3, betas=(0.9, 0.999), eps=1e-08,
                                 weight_decay=0.8, amsgrad=False)
    Hand_joints_list = []
    weights = torch.zeros(len(key_points_2d_lists)*21, 1, dtype=torch.float32)
    Cors_2, confidences_2 = get_Cordinate_2d(key_points_2d_lists[0], 0)

    max_loss = 1000  # 重投影误差 基于视频的连续，上一帧与下一帧的投影误差不会变化太大
    confidence_threshold = 0.6
    for j in range(0, number_frames):
        Cors_2d = np.zeros_like(Cors_2)
        confidences_2d = np.zeros_like(confidences_2)
        not_optied_camera_number = []
        for k in range(0, Camera_number):
            Cors1, confidences1 = get_Cordinate_2d(key_points_2d_lists[k], j)
            if np.mean(confidences1) < confidence_threshold:
                not_optied_camera_number.append(k)
            Cors_2d = np.vstack((Cors_2d, Cors1))
            confidences_2d = np.hstack((confidences_2d, confidences1))
        Cors_2d = np.delete(Cors_2d, [s for s in range(0, Cors_2.shape[0])], axis=0)
        print("根据置信度剔除{}个相机".format(len(not_optied_camera_number)))
        confidences_2d = confidences_2d[:, np.newaxis]
        confidences_2d = np.delete(confidences_2d, [s for s in range(0, confidences_2.shape[0])], axis=0)
        hand_3d_cors, _ = get_Cordinate(Frames_keypoints, j)  # 抽取指定帧用来确定根节点位置

        for k in range(0, Camera_number):
            if k in not_optied_camera_number:
                weights[k * 21:(k + 1) * 21, 0] = 0
            else:
                if Frame_2d_numbers_list[k][j] == j:
                    weights[k * 21:(k + 1) * 21, 0] = 1
                else:
                    weights[k * 21:(k + 1) * 21, 0] = 0
                    print("编号为{}的相机跳帧{}".format(Camera_names[k], j))
        last_loss = 1000
        if first_time:
            first_time = False
        else:
            random_shape.requires_grad = False

        while True:
            optimizer.zero_grad()  # 梯度归0
            hand_verts, hand_joints = mano_layer(random_pose, random_shape)
            hand_cor = hand_joints[0, :, :]  # 21 * 3
            cors = s * torch.from_numpy(R).mm(hand_cor.t()) + torch.from_numpy(t)
            cors = cors.t()
            cors = cors - cors[0] + torch.from_numpy(hand_3d_cors[0])
            # cors = s * R.dot(np.array(hand_cor.detach().numpy(), dtype=np.float32).T) + t  # 将mano手的世界坐标系转化为相机标定时用的世界坐标系
            # cors = cors.T  # 转置成为[-1, 3]的代码
            uv_cor_tmp = Project_to_2d_torch(cors, Camera_matrixs[0], Intrinsics[0])  # 21 * 3
            uv_cor0 = torch.zeros_like(uv_cor_tmp)
            for k in range(0, Camera_number):
                uv_cor1 = Project_to_2d_torch(cors, Camera_matrixs[k], Intrinsics[k])  # 21 * 3
                uv_cor0 = torch.cat((uv_cor0, uv_cor1), dim=0)
            uv_cor0 = uv_cor0[21:, :]
            debug_tmp = torch.mul(torch.mul(torch.sum(loss_fn(uv_cor0[:, 0:2], torch.from_numpy(Cors_2d)), dim=1).unsqueeze(1),
                              torch.from_numpy(confidences_2d)), weights)
            if j >= 1:  # 第一次不做约束
                weights[debug_tmp > max_loss] = 0  # 异常值不参与优化
                if i % 100 == 0:
                    print("{}个相机参与优化".format(torch.sum(weights) / 21))
                # print(weights.size())
            loss = torch.mul(torch.mul(torch.sum(loss_fn(uv_cor0[:, 0:2], torch.from_numpy(Cors_2d)), dim=1).unsqueeze(1),
                              torch.from_numpy(confidences_2d)), weights).mean()

            # loss4 = torch.sum(loss_fn(cors, torch.from_numpy(hand_3d_cors)), dim=1).mean()  # 增加3D点约束
            if i % 100 == 0:
                print("{} loss: {}".format(i, loss.item()))
            loss.backward()
            i = i + 1
            optimizer.step()  # 更新参数
            if np.abs(loss.detach().numpy() - last_loss) < learning_rate or i > 2000:
                print("迭代满足要求，停止迭代")
                writeObj(os.path.join(hand_output_path, "hand-{}.obj".format(j)), hand_verts.detach().numpy()[0, :, :].tolist(), face)
                i = 0
                Hand_joints_list.append(hand_joints.detach().numpy())
                break
            else:
                last_loss = loss.detach().numpy()

    save_pickle_file(os.path.join(hand_output_path, "r_hand.pkl"), Hand_joints_list)

