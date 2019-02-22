import vtk
from util import loadObj
"""
此段程序主要是自动解析obj 并且 通过顶点和点序来自己生成ploygon数据结构来画面片
1、首先将点添加到vtk.vtkPoints()中 设置点
2、vtk.vtkPolygon()设置拓扑结构
3、无论画面还是画线都要将数据描述拓扑构放到vtk.vtkCellArray()中
4、构建polygonPolyData = vtk.vtkPolyData() 
5、设置mapper 构建图形基元
6、mapper给演员
7、建立渲染器
8、建立渲染窗口
9、建立渲染交互式窗口
note: 把mapper之前用来做数据处理，mapper传给actor之后就用来渲染了，所以把mapper作为一个函数是最合适，耦合比较小
"""
def GetPoyMapper(vertexs, faces):
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

    # Create a mapper and actor
    mapper = vtk.vtkPolyDataMapper()
    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(polygonPolyData)
    else:
        mapper.SetInputData(polygonPolyData)
    return mapper


if __name__ == "__main__":
    filenames = ["test.obj"]
    vertexs, faces = loadObj(filenames[0])
    mapper = GetPoyMapper(vertexs, faces)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Visualize
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindowInteractor = vtk.vtkRenderWindowInteractor()
    renderWindowInteractor.SetRenderWindow(renderWindow)

    renderer.AddActor(actor)
    renderer.SetBackground(1, 1, 1) # Background color salmon

    renderWindow.Render()
    renderWindowInteractor.Start()