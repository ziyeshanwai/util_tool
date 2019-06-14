import vtk
import os


def ReadPolyData(file_name):
    path, extension = os.path.splitext(file_name)
    extension = extension.lower()
    if extension == ".ply":
        reader = vtk.vtkPLYReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".vtp":
        reader = vtk.vtkXMLpoly_dataReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".obj":
        reader = vtk.vtkOBJReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutputPort()
    elif extension == ".stl":
        reader = vtk.vtkSTLReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".vtk":
        reader = vtk.vtkpoly_dataReader()
        reader.SetFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    elif extension == ".g":
        reader = vtk.vtkBYUReader()
        reader.SetGeometryFileName(file_name)
        reader.Update()
        poly_data = reader.GetOutput()
    else:
        # Return a None if the extension is unknown.
        poly_data = None
    return poly_data


class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self):
        self.AddObserver('CharEvent', self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)

    def OnCharEvent(self, obj, event):
        pass

    def OnKeyPressEvent(self, obj, event):
        pass


if __name__ == "__main__":
    ColorBackground = [0.0, 0.0, 0.0]
    model_name = os.path.join("./model", "smooth-0.obj")
    jpg_file = os.path.join("./model", "basemesh.jpg")
    reader = vtk.vtkOBJReader()
    reader.SetFileName(model_name)
    reader.Update()
    print("over")
    mapper = vtk.vtkPolyDataMapper()

    if vtk.VTK_MAJOR_VERSION <= 5:
        mapper.SetInput(polyData)
    else:
        mapper.SetInputConnection(reader.GetOutputPort())

    print(reader.GetOutputPort())

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
    actor = vtk.vtkActor()

    actor.SetMapper(mapper)
    actor.SetTexture(texture)

    # Create a rendering window and renderer

    ren = vtk.vtkRenderer()

    ren.SetBackground(ColorBackground)

    renWin = vtk.vtkRenderWindow()
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