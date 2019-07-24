import vtk
import os
import numpy as np
from Util.util import *
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk
from itertools import chain


class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self):
        self.AddObserver('CharEvent', self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        print(key)
        if key == "Left":
            global count
            count += 1
            if os.path.exists(os.path.join(model_path, "{}.obj".format(count))):
                v, f = loadObj(os.path.join(model_path, "{}.obj".format(count)))
                # print(len(v))
                Modify_Vertex(mesh, v, f)
                # accessEachFace(mesh)
                actor.SetMapper(mapper)
                print("{}.obj".format(count))
                renWin.Render()

            if count >= 6000:
                print("replay")
                count = 0
        if key == "Right":
            count -= 1
            if os.path.exists(os.path.join(model_path, "{}.obj".format(count))):
                v, f = loadObj(os.path.join(model_path, "{}.obj".format(count)))
                # print(len(v))
                Modify_Vertex(mesh, v, f)
                # accessEachFace(mesh)
                actor.SetMapper(mapper)
                print("{}.obj".format(count))
                renWin.Render()
            if count <= 0:
                print("replay")
                count = 0
        pass
        
        if key == "Up":
            # global error_frames
            error_frames.append(count)
            print("error_frames add {}".format(count))

        if key == "Down":
            print("error frames:{}".format(error_frames))
            save_pickle_file(os.path.join(error_frames_path, "error_frames.pkl"), error_frames)

        if key == "Delete":
            pop_element = error_frames.pop()
            print("pop the end element {}".format(pop_element))


            


def Modify_Vertex(mesh, to_set_verts, f):
    points = mesh.GetPoints()  # vtkPoints
    verts = mesh.GetVerts()
    # print(mesh.GetNumberOfPoints())
    # print(verts.GetData())
    ver = vtk_to_numpy(verts.GetData())
    # print(ver.shape)
    number_Vertices = points.GetNumberOfPoints()
    using_tex = True
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
count = -1
# model_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\fit_coe_output"
model_path = "\\\\192.168.20.63\\ai\\face_data\\20190514\\wrap"
error_frames_path = "\\\\192.168.20.63\\ai\\face_data\\20190514\\DeepCapture\\DATAROOT\\error_frames"
f = None
error_frames = []
if __name__ == "__main__":
    print("-----------------\n"
          "left play next frame, right play previous frame\n"
          "Up add current frame number to error frame, down save frame_names to local")
    ColorBackground = [0.0, 0.0, 0.0]
    # model_name = os.path.join("./model", "Neutral_face.obj")
    base_face_root = "\\\\192.168.20.63\\ai\\face_data\\20190514\\DeepCapture\\DATAROOT\\BASEFACE"
    uv_model_name = os.path.join(model_path, "{}.obj".format("0"))
    v, f = loadObj(uv_model_name)
    jpg_file = os.path.join(base_face_root, "base.jpg")
    reader = vtk.vtkOBJReader()
    reader.SetFileName(uv_model_name)
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
    reader = vtk.vtkJPEGReader()
    reader.SetFileName(jpg_file)
    # Create texture object
    texture = vtk.vtkTexture()
    if vtk.VTK_MAJOR_VERSION <= 5:
        texture.SetInput(reader.GetOutput())
    else:
        texture.SetInputConnection(reader.GetOutputPort())
    texture.InterpolateOn()
    actor.SetMapper(mapper)
    actor.SetTexture(texture)
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