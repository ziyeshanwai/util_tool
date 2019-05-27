import vtk
import os
import pickle


def save_pickle_file(filename, file):
    with open(filename, 'wb') as f:
        pickle.dump(file, f)
        print("save {}".format(filename))


def load_pickle_file(filename):
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            file = pickle.load(f)
        return file
    else:
        print("{} not exist".format(filename))


def GetTriangleMapper(vertexs, faces):
    points = vtk.vtkPoints()
    for v in vertexs:
        points.InsertNextPoint(v)
    lines = vtk.vtkCellArray()
    line = vtk.vtkLine()
    for f in faces:
        if len(f) == 4:
            line.GetPointIds().SetId(0, f[0] - 1)
            line.GetPointIds().SetId(1, f[1] - 1)
            lines.InsertNextCell(line)
            line.GetPointIds().SetId(0, f[1] - 1)
            line.GetPointIds().SetId(1, f[2] - 1)
            lines.InsertNextCell(line)
            line.GetPointIds().SetId(0, f[2] - 1)
            line.GetPointIds().SetId(1, f[3] - 1)
            lines.InsertNextCell(line)
            line.GetPointIds().SetId(0, f[3] - 1)
            line.GetPointIds().SetId(1, f[1] - 1)
            lines.InsertNextCell(line)
        else:
            if len(f) == 3:
                line.GetPointIds().SetId(0, f[0] - 1)
                line.GetPointIds().SetId(1, f[1] - 1)
                lines.InsertNextCell(line)
                line.GetPointIds().SetId(0, f[1] - 1)
                line.GetPointIds().SetId(1, f[2] - 1)
                lines.InsertNextCell(line)
                line.GetPointIds().SetId(0, f[2] - 1)
                line.GetPointIds().SetId(1, f[0] - 1)
                lines.InsertNextCell(line)

    linesPolyData = vtk.vtkPolyData()
    linesPolyData.SetPoints(points)
    linesPolyData.SetLines(lines)
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(linesPolyData)
    return mapper

def GetFaceMapper(vertexs, faces):
    """
    :param vertexs: obj 顶点
    :param faces: 点序
    :return: 传给actor使用的mapper
    """
    # Setup four points
    points = vtk.vtkPoints()
    for v in vertexs:
        points.InsertNextPoint(v[0], v[1], v[2])  # 设置顶点

    # Create the polygon
    polygon = vtk.vtkPolygon()
    polygon.GetPointIds().SetNumberOfIds(4)
    polygons = vtk.vtkCellArray()  # 设置单元 设置拓扑结构
    for i, f in enumerate(faces):
        if len(f) == 4:
            polygon.GetPointIds().SetId(0, f[0] - 1)
            polygon.GetPointIds().SetId(1, f[1] - 1)
            polygon.GetPointIds().SetId(2, f[2] - 1)
            polygon.GetPointIds().SetId(3, f[3] - 1)
        if len(f) == 3:
            polygon.GetPointIds().SetId(0, f[0] - 1)
            polygon.GetPointIds().SetId(1, f[1] - 1)
            polygon.GetPointIds().SetId(2, f[2] - 1)
        polygons.InsertNextCell(polygon)

    polygonPolyData = vtk.vtkPolyData()
    polygonPolyData.SetPoints(points)
    polygonPolyData.SetPolys(polygons)

    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(polygonPolyData)
    else:
        mapper.SetInputData(polygonPolyData)
    return mapper

def loadObj(path):
    """Load obj file
    读取三角形和四边形的mesh
    返回vertex和face的list
    """
    if path.endswith('.obj'):
        f = open(path, 'r')
        lines = f.readlines()
        vertics = []
        faces = []
        for line in lines:
            if line.startswith('v') and not line.startswith('vt') and not line.startswith('vn'):
                line_split = line.split()
                ver = line_split[1:4]
                ver = [float(v) for v in ver]
                # print(ver)
                vertics.append(ver)
            else:
                if line.startswith('f'):
                    line_split = line.split()
                    if '/' in line:  # 根据需要这里补充obj的其他格式解析
                        tmp_faces = line_split[1:]
                        f = []
                        for tmp_face in tmp_faces:
                            f.append(int(tmp_face.split('/')[0]))
                        faces.append(f)
                    else:
                        face = line_split[1:]
                        face = [int(fa) for fa in face]
                        faces.append(face)
        return vertics, faces

    else:
        print('格式不正确，请检查obj格式')
        return


def writeObj(file_name_path, vertexs, faces):
    """write the obj file to the specific path
       file_name_path:保存的文件路径
       vertexs:顶点数组 list
       faces: 面 list
    """
    with open(file_name_path, 'w') as f:
        for v in vertexs:
            # print(v)
            f.write("v {} {} {}\n".format(v[0], v[1], v[2]))
        for face in faces:
            if len(face) == 4:
                f.write("f {} {} {} {}\n".format(face[0], face[1], face[2], face[3])) # 保存四个顶点
            if len(face) == 3:
                f.write("f {} {} {}\n".format(face[0], face[1], face[2])) # 保存三个顶点
        print("saved mesh to {}".format(file_name_path))

def Quad2Tri(qv, qf):# 将四边形mesh 转化为 三角形mesh
    """
    :param qv: 四边形面的顶点
    :param qf: 四边形面的点序
    :return: 三角形顶点和面片点序以及还原点
    原理是在点序的后面追加点
    点序的分割按照 1 2 3 4---->(1,2,3)(2,3,4)这种方式分割 顶点不变
    """
    trif = []
    self_trif = []
    for face in qf:
        if len(face) == 4:
            f0 = [face[0], face[1], face[2]]
            trif.append(f0)
            f1 = [face[0], face[2], face[3]]
            trif.append(f1)
        else:
            self_trif.append(face)
    index = len(trif)
    tv = qv
    trif.append(self_trif)
    return tv, trif, index


def Tri2Quad(tv, tf, index):  # 将三角mesh 转化为 四边形mesh
    """
    :param tv: 三角形面的的顶点
    :param tf: 三角形边形面的点序
    :index : 还原点 index之后的点序不需要还原
    :return: 四边形顶点和面片点序
    点序的分割按照(1,2,3)(2,3,4)----> 1 2 3 4这种方式分割 顶点不变
    """
    qf = []
    for i in range(0, index, 2):
        qf_tmp = [tf[i][0], tf[i][1], tf[i][2], tf[i+1][2]]
        qf.append(qf_tmp)
    if len(tf) == index:
        pass
    else:
        qf.append(tf[index:])
    return tv, qf


def batch_convert_quad2tri(file_dir, filenames, target_dir):
    """
    description:批量将四边形的面片转化为三角形面片
    :param file_dir: 文件所在目录
    :param filenames: 批量的文件名字
    :param target_dir: 保存的文件夹
    :return: 还原点文件
    """
    index_list = []
    for file in filenames:
        file_path = os.path.join(file_dir, file)
        v, f = loadObj(file_path)
        tv, tf, index = Quad2Tri(v, f)
        writeObj(os.path.join(target_dir, file), tv, tf)
        index_list.append(index)
    save_pickle_file(os.path.join(target_dir, "index.pkl"), index_list)
    return index_list


def batch_convert_tri2quad(file_dir, filenames, target_dir, index):
    """
    description:批量将三角形的面片转化为四边形的面片
    :param file_dir: 文件所在目录
    :param filenames: 批量的文件名字
    :param target_dir: 保存的文件夹
    :param index: 还原点文件
    :return: 返回最后一个测试用例
    """
    for i, file in enumerate(filenames):
        file_path = os.path.join(file_dir, file)
        v, f = loadObj(file_path)
        if isinstance(index,  int):
            qv, qf = Tri2Quad(v, f, index)
        if isinstance(index, list):
            qv, qf = Tri2Quad(v, f, index[i])
        writeObj(os.path.join(target_dir, file), qv, qf)
    return qv, qf


if __name__ == '__main__':
    '''unit test'''
    '''批量转换主程序---------------------------------------------
    file_dir = "C:\\Users\\Administrator\\Desktop\\xiaoyue_OBJ_Seq"
    filenames = ["xiaoyue.0001.obj", "xiaoyue.0002.obj", "xiaoyue.0003.obj", "xiaoyue.0004.obj", "xiaoyue.0005.obj",
                "xiaoyue.0006.obj",
                "xiaoyue.0007.obj", "xiaoyue.0008.obj", "xiaoyue.0009.obj", "xiaoyue.0010.obj", "xiaoyue.0011.obj",
                "xiaoyue.0012.obj",
                "xiaoyue.0013.obj", "xiaoyue.0014.obj"]
    target_dir = "./triangemesh-source"


    index_list = batch_convert_quad2tri(file_dir, filenames, target_dir)
    file_tri = "./triangemesh-source"
    target_file = "./quad_mesh"
    qv, qf = batch_convert_tri2quad(file_tri, filenames, target_file, index_list)
    ------------------------------------
    '''
    # charactor_dir = "charactor"
    # charactor_name = "Xiaoyue_quad.obj"
    # qv, qf = loadObj(os.path.join(charactor_dir, charactor_name))
    # tv, tf, index = Quad2Tri(qv, qf)
    # writeObj(os.path.join(charactor_dir, "Xiaoyue_tri.obj"), tv, tf)
    # save_pickle_file(os.path.join(charactor_dir, 'index.pkl'), index)
    # print(len(tf), index)

    file_dir = "D:\\Blendshape-Based Animation\\charactor_triangles"
    filenames = ["xiaoyue.0001.obj", "xiaoyue.0002.obj", "xiaoyue.0003.obj", "xiaoyue.0004.obj", "xiaoyue.0005.obj",
                 "xiaoyue.0006.obj",
                 "xiaoyue.0007.obj", "xiaoyue.0008.obj", "xiaoyue.0009.obj", "xiaoyue.0010.obj", "xiaoyue.0011.obj",
                 "xiaoyue.0012.obj",
                 "xiaoyue.0013.obj", "xiaoyue.0014.obj"]
    target_dir = "D:\\Blendshape-Based Animation\\charactor_quads"

    index_list = load_pickle_file('D:\\Blendshape-Based Animation\\charactor\\index.pkl')

    qv, qf = batch_convert_tri2quad(file_dir, filenames, target_dir, index_list)

    # v, f = loadObj(os.path.join(file_dir, filenames[0]))

    mapper = GetTriangleMapper(qv, qf)  # 至此load data over
    # mapper = GetTriangleMapper(v, f)  # 至此load data over
    colors = vtk.vtkNamedColors()  # 颜色

    actor = vtk.vtkActor()  # new actor
    actor.SetMapper(mapper)
    actor.GetProperty().SetLineWidth(0.1)
    actor.GetProperty().SetColor(colors.GetColor3d("Peacock"))

    render = vtk.vtkRenderer()  # new renderer
    render.AddActor(actor)
    render.SetBackground(0, 0, 0)  # 设置背景颜色

    renderWindow = vtk.vtkRenderWindow()  # new renderWindow
    renderWindow.AddRenderer(render)
    renderWindow.Render()  # 要先render 才可以显示名字

    renderWindow.SetWindowName("examples")

    irenderWindow = vtk.vtkRenderWindowInteractor()  # new interactive window
    irenderWindow.SetRenderWindow(renderWindow)

    irenderWindow.Initialize()
    irenderWindow.Start()


    # save_path = './test1.obj'
    # writeObj(save_path, v, f)
