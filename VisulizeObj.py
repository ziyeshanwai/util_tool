import vtk
from util import loadObj

# Visualize
colors = vtk.vtkNamedColors()

vertexs, faces = loadObj('./test.obj')

# LineSource:画两个点的线
# def createLine1():
#     lineSource = vtk.vtkLineSource()
#     lineSource.SetPoint1(p1)
#     lineSource.SetPoint2(p2)
#
#     mapper = vtk.vtkPolyDataMapper()
#     mapper.SetInputConnection(lineSource.GetOutputPort())
#     return mapper


# LineSource 多点连续直线
def createLine2():
    lineSource = vtk.vtkLineSource()
    points = vtk.vtkPoints()
    # print(len(vertexs))
    for f in faces:
        if len(f) == 4:
            points.InsertNextPoint(vertexs[f[0]-1])
            points.InsertNextPoint(vertexs[f[1]-1])
            points.InsertNextPoint(vertexs[f[2]-1])
            points.InsertNextPoint(vertexs[f[3]-1])
    lineSource.SetPoints(points)

    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputConnection(lineSource.GetOutputPort())
    return mapper


# LineSource 多点设置几何结构+拓扑结构
def createLine3():
    # Create a vtkPoints object and store the points in it
    points = vtk.vtkPoints()
    for v in vertexs:
        points.InsertNextPoint(v)
        # points.InsertNextPoint(p1)
        # points.InsertNextPoint(p2)
        # points.InsertNextPoint(p3)

    # Create a cell array to store the lines in and add the lines to it
    lines = vtk.vtkCellArray()

    for f in faces:
        if len(f) == 4:
            # print(f)
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, f[0]-1)
            line.GetPointIds().SetId(1, f[1]-1)
            lines.InsertNextCell(line)
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, f[1]-1)
            line.GetPointIds().SetId(1, f[2]-1)
            lines.InsertNextCell(line)
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, f[2]-1)
            line.GetPointIds().SetId(1, f[3]-1)
            lines.InsertNextCell(line)
            line = vtk.vtkLine()
            line.GetPointIds().SetId(0, f[3]-1)
            line.GetPointIds().SetId(1, f[1]-1)
            lines.InsertNextCell(line)

    # Create a polydata to store everything in
    linesPolyData = vtk.vtkPolyData()

    # Add the points to the dataset         几何结构
    linesPolyData.SetPoints(points)

    # Add the lines to the dataset          拓扑结构
    linesPolyData.SetLines(lines)

    # Setup actor and mapper
    mapper = vtk.vtkPolyDataMapper()
    mapper.SetInputData(linesPolyData)
    return mapper


def main():
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(.2, .3, .4)
    # renderer.ResetCamera()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetWindowName("Show mesh")
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)
    # Visualize
    colors = vtk.vtkNamedColors()
    # renderer.SetBackground(colors.GetColor3d("Silver"))

    actor = vtk.vtkActor()
    # 第一种方式
    # actor.SetMapper(createLine1())
    # 第二种方式
    # actor.SetMapper(createLine2())
    # 第三种方式
    actor.SetMapper(createLine3())

    actor.GetProperty().SetLineWidth(0.5)
    actor.GetProperty().SetColor(colors.GetColor3d("Peacock"))
    renderer.AddActor(actor)

    camera = vtk.vtkCamera()
    camera.SetFocalPoint(300, 0, 0)
    camera.SetPosition(0, -0, 0)
    camera.ComputeViewPlaneNormal()
    camera.SetViewUp(0, 1, 0)
    camera.Zoom(0.4)
    renderer.SetActiveCamera(camera)

    renderWindow.Render()
    renderWindowInteractor.Initialize()
    renderWindowInteractor.Start()  # 线程阻塞


if __name__ == '__main__':
    main()
