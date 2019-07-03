import cv2
import os


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


if __name__ == "__main__":

    file_path = "D:\\pycharm_project\\Fit_hands\\manopth\\CameraMatrix"
    file_name = "48072910100.xml"
    node_name = "CameraMatrix"
    xml_file = os.path.join(file_path, file_name)
    came_mat = LoadXML(xml_file, node_name)
    print(came_mat)