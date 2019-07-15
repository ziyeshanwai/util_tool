import vtk
import os
import numpy as np
from Util.util import *
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
from itertools import chain

"""
obj文件具有纹理坐标，即使不使用纹理贴图，obj_reader 也会存储纹理坐标，此时顶点数就会发生变化和util读取得到的顶点数不一致
util读取到的坐标是没有纹理坐标的
"""

class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self):
        self.AddObserver('CharEvent', self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key == "Left":
            global count
            print(count)
            v, f = loadObj(os.path.join(model_path, "hand-{}.obj".format(count)))
            # print(len(v))
            Modify_Vertex(mesh, v, f)
            # accessEachFace(mesh)
            actor.SetMapper(mapper)
            renWin.Render()
            count += 1
            if count >= 4658:
                print("replay")
                count = 0
        pass


def Modify_Vertex(mesh, to_set_verts, f):
    points = mesh.GetPoints()  # vtkPoints
    verts = mesh.GetVerts()
    # print(mesh.GetNumberOfPoints())
    # print(verts.GetData())
    ver = vtk_to_numpy(verts.GetData())
    # print(ver.shape)
    number_Vertices = points.GetNumberOfPoints()
    using_tex = True # obj 文件具有纹理坐标点的顶点数与没有纹理坐标的顶点数不一样
    if len(to_set_verts) == number_Vertices:
        using_tex = False
    # print(number_Vertices)
    # print(len(to_set_verts))
    # verts = []
    # print(f)
    # f = np.array(f, dtype=np.int32)
    # f = f.flatten()
    # f_flaten = [n for c in f for n in c]
    if using_tex:
        f = list(chain((*f)))
    for i in range(0, number_Vertices):
        # x = mesh.GetPoints().GetData().GetComponent(i, 0)
        # y = mesh.GetPoints().GetData().GetComponent(i, 1)
        # z = mesh.GetPoints().GetData().GetComponent(i, 2)
        # verts.append([x, y, z])
        # print(f[i])
        if using_tex:
            mesh.GetPoints().SetPoint(i, to_set_verts[f[i] - 1][0], to_set_verts[f[i] - 1][1],
                                      to_set_verts[f[i] - 1][2])
        else:
            mesh.GetPoints().SetPoint(i, to_set_verts[i][0], to_set_verts[i][1], to_set_verts[i][2])
    # writeObj("./model/test.obj", verts, f)
    mesh.GetPoints().Modified()  # 不写会没有反应

def accessEachFace(mesh):
    numberOfFaces = mesh.GetNumberOfCells()
    for i in range(0, numberOfFaces):
        face = vtk.vtkIdList()
        mesh.GetCellPoints(i, face)
        for j in range(0, face.GetNumberOfIds()):
            # id0 = face.GetId(0)
            # id1 = face.GetId(1)
            # id2 = face.GetId(2)
            # id3 = face.GetId(3)
            print("{}".format(face.GetId(j)))
        print("-------------")


mapper = vtk.vtkPolyDataMapper()
actor = vtk.vtkActor()
mesh = None
reader = vtk.vtkOBJReader()
renWin = vtk.vtkRenderWindow()
count = 0
# model_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\fit_coe_output"
model_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\Hand_Data\\output_transform_5"
f = None

if __name__ == "__main__":
    ColorBackground = [0.0, 0.0, 0.0]
    # model_name = os.path.join("./model", "Neutral_face.obj")
    model_name = os.path.join(model_path, "hand-{}.obj".format("0"))
    v, f = loadObj(model_name)
    # jpg_file = os.path.join("./model", "basemesh.jpg")
    reader = vtk.vtkOBJReader()
    reader.SetFileName(model_name)
    reader.Update()
    # print(count)
    """
    get the vertex infomation
    """
    mesh = reader.GetOutput()  # vtkPolyData
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(polyData)
    else:
        mapper.SetInputConnection(reader.GetOutputPort())
    """
    add texture
    """
    # reader = vtk.vtkJPEGReader()
    # reader.SetFileName(jpg_file)
    # Create texture object
    # texture = vtk.vtkTexture()
    # if vtk.VTK_MAJOR_VERSION <= 5:
    #     texture.SetInput(reader.GetOutput())
    # else:
    #     texture.SetInputConnection(reader.GetOutputPort())
    # texture.InterpolateOn()
    actor.SetMapper(mapper)
    # actor.SetTexture(texture)
    # Create a rendering window and renderer
    ren = vtk.vtkRenderer()
    ren.SetBackground(ColorBackground)
    renWin.SetSize(960, 960)
    renWin.AddRenderer(ren)
    # Create a renderwindowinteractor
    mystyle = MyInteractor()
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetInteractorStyle(mystyle)
    iren.SetRenderWindow(renWin)
    # Assign actor to the renderer
    ren.AddActor(actor)
    # Enable user interface interactor
    iren.Initialize()
    renWin.Render()
    iren.Start()