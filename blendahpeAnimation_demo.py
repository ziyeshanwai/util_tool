
import sys
from PyQt5 import QtWidgets
from PyQT_form import Ui_Form
from util import *
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtk.util.colors import *


class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self):
        self.AddObserver('CharEvent', self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        pass


class Blendshape(object):

    def __init__(self, file_names, mean_file_name):
        self.verts = []
        self.face = None
        for file in file_names:
            v, f = loadObj(file)
            self.verts.append(np.array(v))
        self.face = f
        self.number_blendshapes = len(self.verts)
        self.weights = np.zeros((self.number_blendshapes,), dtype=np.float32)
        self.sum_blendshapes = np.zeros_like(np.array(v), dtype=np.float32)
        self.mean_value = self.Get_mean_valule(mean_file_name)

    def Get_mean_valule(self, mean_mesh_file):
        v, f = loadObj(mean_mesh_file)
        return np.array(v, dtype=np.float32)



class MyPyQT_Form(QtWidgets.QWidget, Ui_Form, Blendshape):
    def __init__(self, file_names, mean_file_name):
        super(MyPyQT_Form, self).__init__()
        super(Ui_Form, self).__init__(file_names, mean_file_name)
        self.setupUi(self)
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()
        self.vtkWidget.resize(999, 1109)  # 设置vtk 交互窗口大小
        self.camera = vtk.vtkCamera()
        self.actor = vtk.vtkActor()
        self.loadActor()
        self.CreateScene()

    def slider1_value_changed(self, value):
        self.textEdit.setText("value is {}".format(value/100))
        self.weights[0] = value/100
        tmp = [self.weights[i] * self.verts[i] for i in range(0, self.number_blendshapes)]
        self.sum_blendshapes = sum(tmp) + self.mean_value
        print(self.sum_blendshapes.shape)
        self.set_Actor_mapper()

    def slider2_value_changed(self, value):
        self.textEdit.setText("value is {}".format(value/100))
        self.weights[1] = value/100
        tmp = [self.weights[i] * self.verts[i] for i in range(0, self.number_blendshapes)]
        self.sum_blendshapes = sum(tmp) + self.mean_value
        self.set_Actor_mapper()

    def slider3_value_changed(self, value):
        self.textEdit.setText("value is {}".format(value/100))
        self.weights[2] = value/100
        tmp = [self.weights[i] * self.verts[i] for i in range(0, self.number_blendshapes)]
        self.sum_blendshapes = sum(tmp) + self.mean_value
        self.set_Actor_mapper()

    def slider4_value_changed(self, value):
        self.textEdit.setText("value is {}".format(value/100))
        self.weights[3] = value/100
        tmp = [self.weights[i] * self.verts[i] for i in range(0, self.number_blendshapes)]
        self.sum_blendshapes = sum(tmp) + self.mean_value
        self.set_Actor_mapper()

    def CreateGround(self):
        plane = vtk.vtkPlaneSource()
        plane.SetXResolution(50)
        plane.SetYResolution(50)
        plane.SetCenter(0, 0, 0)
        plane.SetNormal(0, 0, 1)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(plane.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetRepresentationToWireframe()
        actor.GetProperty().SetColor(light_grey)
        transform = vtk.vtkTransform()
        transform.Scale(2000, 2000, 1)
        actor.SetUserTransform(transform)
        return actor

    def CreateScene(self):
        style = MyInteractor()
        self.iren.SetInteractorStyle(style)  # 设置交互方式
        self.ren.SetBackground(.2, .2, .2)
        ground = self.CreateGround()
        self.ren.AddActor(ground)
        self.camera.SetViewAngle(30)
        self.camera.SetFocalPoint(300, 0, 0)
        self.camera.SetPosition(600, -800, 700)
        self.camera.ComputeViewPlaneNormal()
        self.camera.SetViewUp(0, 0, 0)
        self.camera.Zoom(0.4)
        self.ren.SetActiveCamera(self.camera)
        self.iren.Initialize()
        self.iren.Start()

    def loadActor(self):
        mapper = GetFaceMapper(self.mean_value, self.face)
        self.actor.SetMapper(mapper)
        r = vtk.vtkMath.Random(.4, 1.0)
        g = vtk.vtkMath.Random(.4, 1.0)
        b = vtk.vtkMath.Random(.4, 1.0)
        self.actor.GetProperty().SetDiffuseColor(r, g, b)
        self.actor.GetProperty().SetDiffuse(.8)
        self.actor.GetProperty().SetSpecular(.5)
        self.actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
        self.actor.GetProperty().SetSpecularPower(30.0)
        self.actor.RotateX(0)
        transform = vtk.vtkTransform()
        transform.Scale(50, 50, 50)
        self.actor.SetUserTransform(transform)
        self.actor.SetPosition(-0.5, -7, 1)
        self.ren.AddActor(self.actor)

    def set_Actor_mapper(self):
        mapper = GetFaceMapper(self.sum_blendshapes, self.face)
        print("hello")
        self.actor.SetMapper(mapper)
        # self.iren.ReInitialize()
        self.iren.Render()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    file_names = [os.path.join("./Models", "1.obj"), os.path.join("./Models", "2.obj"), os.path.join("./Models", "3.obj"), os.path.join("./Models", "4.obj")]
    mean_file = os.path.join("./models", "0.obj")
    my_pyqt_form = MyPyQT_Form(file_names, mean_file)
    my_pyqt_form.show()
    sys.exit(app.exec_())