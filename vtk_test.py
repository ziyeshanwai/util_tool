
import vtk
import os
import time



if __name__ == '__main__':

     ColorBackground = [0.0, 0.0, 0.0]
     ren = vtk.vtkRenderer()

     ren.SetBackground(ColorBackground)

     renWin = vtk.vtkRenderWindow()

     renWin.AddRenderer(ren)


     FirstobjPath = r"C:\\Users\\Administrator\\Desktop\\Object1011(1).obj"

     reader = vtk.vtkOBJReader()
     for i in range(1, 10):

          reader.SetFileName(FirstobjPath.format(i))

          # reader.Update()

          mapper = vtk.vtkPolyDataMapper()

          if vtk.VTK_MAJOR_VERSION <= 5:

               mapper.SetInput(reader.GetOutput())

          else:
               mapper.SetInputConnection(reader.GetOutputPort())
               # print(reader.GetOutput())
               print('---------------------------')
          actor = vtk.vtkActor()
          actor.SetMapper(mapper)

          # Create a rendering window and renderer



          # Create a renderwindowinteractor

          # iren = vtk.vtkRenderWindowInteractor()
          #
          # iren.SetRenderWindow(renWin)

          # Assign actor to the renderer

          ren.AddActor(actor)

          # Enable user interface interactor

          # iren.Initialize()

          renWin.Render()
          time.sleep(0.1)

     os.system('pause')

     # iren.Start()