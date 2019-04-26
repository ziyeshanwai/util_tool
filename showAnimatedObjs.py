import vtk
from util import GetTriangleMapper, GetFaceMapper
from vtk.util.colors import *
from util import loadObj
import os
import numpy as np
import time
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk


start = False


actor_dir = "\\\\192.168.80.195\data3\LiyouWang\AlignedHead"
# actor_dir = "\\\\192.168.80.195\\data\\photoscan\\2019-04-19\\1\\wrap_data"
filenames = [actor_dir + "\\0.obj"]

filename = [str(i)+".obj" for i in range(0, 501)]

exitFlag = 0
renWin = vtk.vtkRenderWindow()
v = list()
f = None
actor = list()  # the list of links
for file in filename:  # 加载第一个模型
    pt = os.path.join(actor_dir, file)
    if os.path.exists(pt):
        ver, f = loadObj(pt)
        v.append(np.array(ver))
        print("append {}".format(pt))
    else:
        print("{} is not exist".format(file))


class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("CharEvent", self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)
        self.i = 0

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if (key == "Left"):
            mapper1 = GetFaceMapper(v[self.i], f)
            actor[0].SetMapper(mapper1)
            self.i += 1
            if self.i >= len(v):
                self.i = 0
            renWin.Render()

        if (key == "Right"):
            pass

        if (key == "Up"):
            pass

        if (key == "Down"):
            pass

        # Ask each renderer owned by this RenderWindow to render its image and synchronize this process
        renWin.Render()
        return


def LoadModel(filename):

    v, f = loadObj(filename)
    mapper = GetFaceMapper(v, f)
    actor = vtk.vtkLODActor()
    actor.SetMapper(mapper)
    return actor  # represents an entity in a rendered scene


def CreateCoordinates():
    # create coordinate axes in the render window
    axes = vtk.vtkAxesActor()
    axes.SetTotalLength(50, 50, 50)  # Set the total length of the axes in 3 dimensions

    # Set the type of the shaft to a cylinder:0, line:1, or user defined geometry.
    axes.SetShaftType(0)
    tprop = vtk.vtkTextProperty()
    tprop.SetFontSize(1)  # seems to be overriden by vtkCaptionActor2D
    # tprop.SetBold(1)
    # tprop.SetItalic(0)
    # tprop.SetColor(1.0, 1.0, 1.0)
    # tprop.SetOpacity(1.0)
    # tprop.SetFontFamilyToTimes()

    axes.SetCylinderRadius(0.02)
    # axes.GetXAxisCaptionActor2D().SetFontSize(10)
    # axes.GetYAxisCaptionActor2D().GetTextProperty().SetFontSize(10)
    # axes.GetZAxisCaptionActor2D().GetTextProperty().SetFontSize(10)
    axes.GetXAxisCaptionActor2D().SetWidth(0.03)
    axes.GetYAxisCaptionActor2D().SetWidth(0.03)
    axes.GetZAxisCaptionActor2D().SetWidth(0.03)
    for label in [
        axes.GetXAxisCaptionActor2D(),
        axes.GetYAxisCaptionActor2D(),
        axes.GetZAxisCaptionActor2D(),
    ]:

        label.SetCaptionTextProperty(tprop)
    # axes.SetAxisLabels(0)  # Enable:1/disable:0 drawing the axis labels
    # transform = vtk.vtkTransform()
    # transform.Translate(0.0, 0.0, 0.0)
    # axes.SetUserTransform(transform)
    # axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().SetColor(1,0,0)
    # axes.GetXAxisCaptionActor2D().GetCaptionTextProperty().BoldOff() # disable text bolding
    return axes


def CreateGround():
    # create plane source
    plane = vtk.vtkPlaneSource()
    plane.SetXResolution(50)
    plane.SetYResolution(50)
    plane.SetCenter(0, 0, 0)
    plane.SetNormal(0, 0, 1)

    # mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(plane.GetOutputPort())

    # actor
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetRepresentationToWireframe()
    # actor.GetProperty().SetOpacity(0.4)  # 1.0 is totally opaque and 0.0 is completely transparent
    actor.GetProperty().SetColor(light_grey)

    '''
    # Load in the texture map. A texture is any unsigned char image.
    bmpReader = vtk.vtkBMPReader()  
    bmpReader.SetFileName("ground_texture.bmp")  
    texture = vtk.vtkTexture()  
    texture.SetInputConnection(bmpReader.GetOutputPort())  
    texture.InterpolateOn()  
    actor.SetTexture(texture)  # 设置纹理
    '''
    transform = vtk.vtkTransform()
    transform.Scale(2000, 2000, 1)
    actor.SetUserTransform(transform)

    return actor


def CreateScene():
    # Create a rendering window and renderer
    ren = vtk.vtkRenderer()
    # renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(ren)
    renWin.Render()
    renWin.SetWindowName("deformation transfer")

    # Create a renderwindowinteractor
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    style = MyInteractor()
    style.SetDefaultRenderer(ren)
    iren.SetInteractorStyle(style)

    for id, file in enumerate(filenames):
        actor.append(LoadModel(file))  # load model
        # actor[id].GetProperty().SetColor(blue)
        r = vtk.vtkMath.Random(.4, 1.0)
        g = vtk.vtkMath.Random(.4, 1.0)
        b = vtk.vtkMath.Random(.4, 1.0)
        actor[id].GetProperty().SetDiffuseColor(r, g, b)
        actor[id].GetProperty().SetDiffuse(.8)
        actor[id].GetProperty().SetSpecular(.5)
        actor[id].GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
        actor[id].GetProperty().SetSpecularPower(30.0)


    actor[0].RotateX(0)
    transform = vtk.vtkTransform()
    transform.Scale(50, 50, 50)
    actor[0].SetUserTransform(transform)
    actor[0].SetPosition(-0.5, -7, 1)

    ren.AddActor(actor[0])
    ground = CreateGround()  # 实际上ground 就是actor
    ren.AddActor(ground)

    # Set background color
    ren.SetBackground(.2, .2, .2)

    # Set window size
    renWin.SetSize(1500, 900)  # width height

    # Set up the camera to get a particular view of the scene
    camera = vtk.vtkCamera()
    camera.SetViewAngle(30)
    camera.SetFocalPoint(300, 0, 0)
    camera.SetPosition(300, -400, 350)
    camera.ComputeViewPlaneNormal()
    camera.SetViewUp(0, 0, 0)
    camera.Zoom(0.4)
    ren.SetActiveCamera(camera)

    iren.Initialize()

    iren.Start()  # 这行代码会阻塞事件


if __name__ == "__main__":
    CreateScene()