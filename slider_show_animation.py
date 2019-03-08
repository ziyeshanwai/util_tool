import vtk
from util import GetTriangleMapper, GetFaceMapper
from vtk.util.colors import *
from util import loadObj
import os
import numpy as np
from vtk.util.numpy_support import vtk_to_numpy, numpy_to_vtk


filenames = ["C:\\Users\\Administrator\\Desktop\\xiaoyue_OBJ_Seq\\xiaoyue.0013.obj", "D:\\Blendshape-Animation\\Transfered\\Small_sister1\\Charactor\\Quad\\xiaoyue.0013.obj"]
filedir = "C:\\Users\\Administrator\\Desktop\\xiaoyue_OBJ_Seq"
filename = ["xiaoyue.0001.obj", "xiaoyue.0002.obj", "xiaoyue.0003.obj", "xiaoyue.0004.obj", "xiaoyue.0005.obj", "xiaoyue.0006.obj",
            "xiaoyue.0007.obj", "xiaoyue.0008.obj", "xiaoyue.0009.obj", "xiaoyue.0010.obj", "xiaoyue.0011.obj", "xiaoyue.0012.obj",
            "xiaoyue.0013.obj", "xiaoyue.0014.obj"]
charactor_blendshape_dir = "D:\\Blendshape-Animation\\Transfered\\Small_sister1\\Charactor\\Quad"
exitFlag = 0
dt = 1.0  # degree step in rotation
angle = [0, 0]  # shoulder and elbow joint angle
pose = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
renWin = vtk.vtkRenderWindow()
assembly = vtk.vtkAssembly()
v = list()
f = None
actor = list()  # the list of links
for file in filename:  # 加载第一个模型
    pt = os.path.join(filedir, file)
    ver, f = loadObj(pt)
    v.append(np.array(ver))

v2 = list()
f2 = None
for file in filename:  # 加载第一个模型
    pt = os.path.join(charactor_blendshape_dir, file)
    ver, f2 = loadObj(pt)
    v2.append(np.array(ver))

class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, parent=None):
        self.AddObserver("CharEvent", self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        global angle
        key = self.GetInteractor().GetKeySym()

        if (key == "Left"):
           pass

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


def para1_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[0] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v/len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i]*(v[i]-tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)
    print("pose: {}".format(pose))

    renWin.Render()


def para2_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[1] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()

def para3_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[2] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para4_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[3] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para5_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[4] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para6_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[5] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para7_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[6] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para8_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[7] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para9_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[8] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para10_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[9] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para11_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[10] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para12_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[11] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para13_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[12] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def para14_Callback(obj, event):
    sliderRepres = obj.GetRepresentation()
    pose[13] = sliderRepres.GetValue()
    sum_v = np.zeros_like(v[0])
    for i in range(0, len(v)):
        sum_v += v[i]
    tmp = sum_v / len(v)
    vv = np.zeros_like(v[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f)
    actor[0].SetMapper(mapper)

    sum_v = np.zeros_like(v2[0])
    for i in range(0, len(v2)):
        sum_v += v2[i]
    tmp = sum_v / len(v2)
    vv = np.zeros_like(v2[0])
    for i in range(0, len(pose)):
        vv += pose[i] * (v2[i] - tmp)
    vv = vv + tmp
    mapper = GetFaceMapper(vv, f2)
    actor[1].SetMapper(mapper)

    print("pose: {}".format(pose))
    renWin.Render()


def ConfigSlider(sliderRep, TitleText, Yaxes, origin, length):
    sliderRep.SetMinimumValue(0.0)
    sliderRep.SetMaximumValue(1.0)
    sliderRep.SetValue(0.0)  # Specify the current value for the widgetGe
    sliderRep.SetTitleText(TitleText)  # Specify the label text for this widget
    # sliderRep.GetSliderProperty().SetFontSize(1)
    # sliderRep.GetSliderProperty().Set

    sliderRep.GetSliderProperty().SetColor(1, 0, 0)  # Change the color of the knob that slides
    sliderRep.GetSelectedProperty().SetColor(0, 0, 1)  # Change the color of the knob when the mouse is held on it
    sliderRep.GetTubeProperty().SetColor(1, 1, 0)  # Change the color of the bar
    sliderRep.GetCapProperty().SetColor(0, 1, 1)  # Change the color of the ends of the bar
    # sliderRep.GetTitleProperty().SetColor(1,0,0)  # Change the color of the text displaying the value

    # Position the first end point of the slider
    sliderRep.GetPoint1Coordinate().SetCoordinateSystemToDisplay()
    sliderRep.GetPoint1Coordinate().SetValue(origin, Yaxes)

    # Position the second end point of the slider
    sliderRep.GetPoint2Coordinate().SetCoordinateSystemToDisplay()
    sliderRep.GetPoint2Coordinate().SetValue(origin + length, Yaxes)

    sliderRep.SetSliderLength(0.005)  # Specify the length of the slider shape.The slider length by default is 0.05
    sliderRep.SetSliderWidth(0.005)  # Set the width of the slider in the directions orthogonal to the slider axis
    sliderRep.SetTubeWidth(0.0005)
    sliderRep.SetEndCapWidth(0.003)

    sliderRep.ShowSliderLabelOn()  # display the slider text label
    sliderRep.SetLabelFormat("%.1f")

    sliderWidget = vtk.vtkSliderWidget()
    sliderWidget.SetRepresentation(sliderRep)
    sliderWidget.SetAnimationModeToAnimate()

    return sliderWidget


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
    renWin.SetWindowName("blendshape rig transfer system")

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


    actor[0].RotateX(80)
    transform = vtk.vtkTransform()
    transform.Scale(10, 10, 10)
    actor[0].SetUserTransform(transform)

    actor[1].RotateX(80)
    transform = vtk.vtkTransform()
    transform.Scale(10, 10, 10)
    actor[1].SetUserTransform(transform)
    actor[1].SetPosition(20, 0, 0)


    ren.AddActor(actor[0])
    ren.AddActor(actor[1])

    # Add coordinates
    # axes = CreateCoordinates()
    # ren.AddActor(axes)

    # Add ground
    ground = CreateGround()  # 实际上ground 就是actor
    ren.AddActor(ground)

    # Add slider to control the robot 交互事件注册
    para1 = vtk.vtkSliderRepresentation2D()
    para2 = vtk.vtkSliderRepresentation2D()
    para3 = vtk.vtkSliderRepresentation2D()
    para4 = vtk.vtkSliderRepresentation2D()
    para5 = vtk.vtkSliderRepresentation2D()
    para6 = vtk.vtkSliderRepresentation2D()
    para7 = vtk.vtkSliderRepresentation2D()
    para8 = vtk.vtkSliderRepresentation2D()
    para9 = vtk.vtkSliderRepresentation2D()
    para10 = vtk.vtkSliderRepresentation2D()
    para11 = vtk.vtkSliderRepresentation2D()
    para12 = vtk.vtkSliderRepresentation2D()
    para13 = vtk.vtkSliderRepresentation2D()
    para14 = vtk.vtkSliderRepresentation2D()

    ori = 2
    length = 80

    sliderWidget_para1 = ConfigSlider(para1, "para_1", 60, ori, length)
    sliderWidget_para1.SetInteractor(iren)
    sliderWidget_para1.EnabledOn()
    sliderWidget_para1.AddObserver("InteractionEvent", para1_Callback)  # 事件注册

    sliderWidget_para2 = ConfigSlider(para2, "para_2", 140, ori, length)
    sliderWidget_para2.SetInteractor(iren)
    sliderWidget_para2.EnabledOn()
    sliderWidget_para2.AddObserver("InteractionEvent", para2_Callback)

    sliderWidget_para3 = ConfigSlider(para3, "para_3", 220, ori, length)
    sliderWidget_para3.SetInteractor(iren)
    sliderWidget_para3.EnabledOn()
    sliderWidget_para3.AddObserver("InteractionEvent", para3_Callback)

    sliderWidget_para4 = ConfigSlider(para4, "para_4", 300, ori, length)
    sliderWidget_para4.SetInteractor(iren)
    sliderWidget_para4.EnabledOn()
    sliderWidget_para4.AddObserver("InteractionEvent", para4_Callback)

    sliderWidget_para5 = ConfigSlider(para5, "para_5", 380, ori, length)
    sliderWidget_para5.SetInteractor(iren)
    sliderWidget_para5.EnabledOn()
    sliderWidget_para5.AddObserver("InteractionEvent", para5_Callback)

    sliderWidget_para6 = ConfigSlider(para6, "para_6", 460, ori, length)
    sliderWidget_para6.SetInteractor(iren)
    sliderWidget_para6.EnabledOn()
    sliderWidget_para6.AddObserver("InteractionEvent", para6_Callback)

    sliderWidget_para7 = ConfigSlider(para7, "para_7", 540, ori, length)
    sliderWidget_para7.SetInteractor(iren)
    sliderWidget_para7.EnabledOn()
    sliderWidget_para7.AddObserver("InteractionEvent", para7_Callback)

    sliderWidget_para8 = ConfigSlider(para8, "para_8", 620, ori, length)
    sliderWidget_para8.SetInteractor(iren)
    sliderWidget_para8.EnabledOn()
    sliderWidget_para8.AddObserver("InteractionEvent", para8_Callback)

    sliderWidget_para9 = ConfigSlider(para9, "para_9", 700, ori, length)
    sliderWidget_para9.SetInteractor(iren)
    sliderWidget_para9.EnabledOn()
    sliderWidget_para9.AddObserver("InteractionEvent", para9_Callback)

    sliderWidget_para10 = ConfigSlider(para10, "para_10", 780, ori, length)
    sliderWidget_para10.SetInteractor(iren)
    sliderWidget_para10.EnabledOn()
    sliderWidget_para10.AddObserver("InteractionEvent", para10_Callback)

    delta = 100
    sliderWidget_para11 = ConfigSlider(para11, "para_11", 60, ori + delta, length)
    sliderWidget_para11.SetInteractor(iren)
    sliderWidget_para11.EnabledOn()
    sliderWidget_para11.AddObserver("InteractionEvent", para10_Callback)

    sliderWidget_para12 = ConfigSlider(para12, "para_12", 140, ori + delta, length)
    sliderWidget_para12.SetInteractor(iren)
    sliderWidget_para12.EnabledOn()
    sliderWidget_para12.AddObserver("InteractionEvent", para11_Callback)

    sliderWidget_para13 = ConfigSlider(para13, "para_13", 220, ori + delta, length)
    sliderWidget_para13.SetInteractor(iren)
    sliderWidget_para13.EnabledOn()
    sliderWidget_para13.AddObserver("InteractionEvent", para12_Callback)

    sliderWidget_para14 = ConfigSlider(para14, "para_14", 300, ori + delta, length)
    sliderWidget_para14.SetInteractor(iren)
    sliderWidget_para14.EnabledOn()
    sliderWidget_para14.AddObserver("InteractionEvent", para13_Callback)

    # Set background color
    ren.SetBackground(.2, .2, .2)

    # Set window size
    renWin.SetSize(1500, 900)  # width height

    # transform = vtk.vtkTransform()
    # transform.Scale(100, 100, 100)

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