import vtk
 
cone_a=vtk.vtkConeSource()
 
coneMapper = vtk.vtkPolyDataMapper()
coneMapper.SetInputConnection(cone_a.GetOutputPort())
 
coneActor = vtk.vtkActor()
coneActor.SetMapper(coneMapper)
 
 
ren1= vtk.vtkRenderer()
ren1.AddActor( coneActor )
ren1.SetBackground( 0.1, 0.2, 0.4 )
 
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer( ren1 )
renWin.SetSize( 300, 300 )
renWin.Render()
 
iren=vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
 
iren.Initialize()
iren.Start()