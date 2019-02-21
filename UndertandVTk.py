import os

import vtk


base_file = "C:\\Users\\Administrator\\Desktop\\xiaoyue_OBJ_Seq"
test_file = "xiaoyue.0001.obj"
actor = vtk.vtkActor()
renWin = vtk.vtkRenderWindow()

"""
此段程序的功能为基于vtk 制作的模型观察器，通过加入鼠标事件，只有在点击鼠标时模型才会发生转动
同时也是为了更好的理解VTK，这是我接触VTK的第二天
关于VTK的一些理解：VTK 做显示的pipline
1、reader = vtk.vtkOBJReader() 首先有个reader对象，用来读取模型数据
2、mapper = vtk.vtkPolyDataMapper() 将读取的数据转化为图形基元
3、actor = vtk.vtkActor() 将mapper赋予给演员 演员就可以把读取的数据显示出来了actor可以理解为要显示在场景中的一个抽象的载体，可以
修改她的一些属性，比如线条的颜色和宽细等等
4、render = vtk.vtkRenderer() 渲染器 这个抽象的家伙渲染actor
5、renWin = vtk.vtkRenderWindow() 渲染结果的载体，render 传给他
6、iren = vtk.vtkRenderWindowInteractor() 将第五步中的renWin作为参数传入，创建一个交互式渲染窗口，这样就用户就可以用鼠标控制了
7、note： 一个程序中可以有很多actor，但是只能有一个渲染窗口和一个渲染器
8、vtk 使用自己内部的数据结构，比如定义点和线什么的，不能用list 结构,需要先声明一个vtk对象，然后再将list数据插入到对象中
"""

def show(file_name):
     # load  obj file
     reader = vtk.vtkOBJReader()
     reader.SetFileName(file_name)

     mapper = vtk.vtkPolyDataMapper()
     mapper.SetInputConnection(reader.GetOutputPort())
     reader.

     actor.SetMapper(mapper)
     # actor.RotateY(45)

     # Create  renderer
     # Assign actor to the renderer
     ren = vtk.vtkRenderer()
     ren.AddActor(actor)

     # create a rendering window
     # renWin = vtk.vtkRenderWindow()
     renWin.AddRenderer(ren)

     # Create a renderwindowinteractor
     iren = vtk.vtkRenderWindowInteractor()
     iren.SetRenderWindow(renWin)
     camera = vtk.vtkCamera()
     camera.SetFocalPoint(0, 0, 0)
     camera.SetPosition(0, -0, 50)
     camera.ComputeViewPlaneNormal()
     camera.SetViewUp(0, 1, 0)
     camera.Zoom(0.4)
     ren.SetActiveCamera(camera)


     # Enable user interface interactor
     iren.Initialize()
     renWin.Render()
     iren.SetInteractorStyle(MyEvent())
     iren.Start()
     # 引入上一段程式碼呼叫
     #
     return iren


# 繞x軸旋轉
def rotate_x(num):
     actor.RotateX(num)


def rotate_y(num):
     actor.RotateY(num)


def rotate_z(num):
     actor.RotateZ(num)


# 設定方向
def set_origin(x, y, z):
     actor.SetOrientation(x, y, z)


def get_origin():
     return actor.GetOrientation()


# 縮放
def set_scale(x, y, z):
     actor.SetScale(x, y, z)


def main():
     show(os.path.join(base_file, test_file))


# 监听事件
class MyEvent(vtk.vtkInteractorStyleTrackballCamera):

     def __init__(self, parent=None):
          # 滑鼠中鍵
          self.AddObserver("MiddleButtonPressEvent", self.middle_button_press_event)
          self.AddObserver("MiddleButtonReleaseEvent", self.middle_button_release_event)
          # 滑鼠左鍵
          self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
          self.AddObserver("LeftButtonReleaseEvent", self.left_button_release_event)
          # 滑鼠右鍵
          self.AddObserver("RightButtonPressEvent", self.right_button_press_event)
          self.AddObserver("RightButtonReleaseEvent", self.right_button_release_event)
          # 键盘事件
          self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

     def middle_button_press_event(self, obj, event):
          print("Middle Button pressed")
          self.OnMiddleButtonDown()
          return

     def middle_button_release_event(self, obj, event):
          print("Middle Button released")
          self.OnMiddleButtonUp()
          return

     def left_button_press_event(self, obj, event):
          print("Left Button pressed")
          self.OnLeftButtonDown()
          return

     def left_button_release_event(self, obj, event):
          print("Left Button released")
          self.OnLeftButtonUp()
          return

     def right_button_press_event(self, obj, event):
          print("right Button pressed")
          self.OnRightButtonDown()
          return

     def right_button_release_event(self, obj, event):
          print("right Button released")
          self.OnLeftButtonUp()
          return

     def OnKeyPressEvent(self, obj, event):
          key = self.GetInteractor().GetKeySym()
          if key == "Left":
               print("key left")
               rotate_x(5)

          if key == "Right":
               print("key right")
               rotate_y(5)

          if key == "Up":
               print("key up")
               rotate_z(5)

          if key == "Down":
               set_origin(0, 0, 0)

          renWin.Render()  # 重新渲染窗口


if __name__ == '__main__':
     main()