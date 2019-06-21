from Util.util import *
from itertools import chain
import cv2

class MyInteractor(vtk.vtkInteractorStyleTrackballCamera):

    def __init__(self):
        self.AddObserver('CharEvent', self.OnCharEvent)
        self.AddObserver("KeyPressEvent", self.OnKeyPressEvent)
        self.image_path = "\\\\192.168.20.63\\ai\\face_data\\20190514\\image\\048170110027"
        self.cv2_window = cv2.namedWindow("image")
        self.AddObserver("TimerEvent", self.execute)

    def OnCharEvent(self, obj, event):
        pass

    def execute(self, obj, event):
        print("sss...")
        global count
        print("count is {}".format(count))
        calculated_mesh = coes[count].dot(delta_V) + b0[np.newaxis, :]
        v = calculated_mesh.reshape(-1, 3)
        Modify_Vertex(mesh, v, f0)
        # accessEachFace(mesh)
        actor.SetMapper(mapper)
        renWin.Render()
        img_file = os.path.join(self.image_path, "{}.jpg".format(count))
        img = cv2.imread(img_file)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.T  # 取决于图片是不是倒着的
        img = cv2.resize(img, dsize=(258, 386))
        cv2.imshow("image", img)
        # cv2.waitKey(1)
        count += 1
        if count >= 1121:
            print("replay")
            count = 0

    def OnKeyPressEvent(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key == "Left":
            global count
            print("count is {}".format(count))
            calculated_mesh = coes[count].dot(delta_V) + b0[np.newaxis, :]
            v = calculated_mesh.reshape(-1, 3)
            Modify_Vertex(mesh, v, f0)
            # accessEachFace(mesh)
            actor.SetMapper(mapper)
            renWin.Render()
            img_file = os.path.join(self.image_path, "{}.jpg".format(count))
            img = cv2.imread(img_file)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            img = img.T  # 取决于图片是不是倒着的
            img = cv2.resize(img, dsize=(258, 386))
            cv2.imshow("image", img)
            # cv2.waitKey(1)
            count += 1
            if count >= 1121:
                print("replay")
                count = 0
        pass


def Modify_Vertex(mesh, to_set_verts, f):
    points = mesh.GetPoints()  # vtkPoints
    number_Vertices = points.GetNumberOfPoints()
    f = list(chain((*f)))
    for i in range(0, number_Vertices):
        mesh.GetPoints().SetPoint(i, to_set_verts[f[i]-1][0], to_set_verts[f[i]-1][1], to_set_verts[f[i]-1][2])
    mesh.GetPoints().Modified()  # 不写会没有反应

v0 = None
f0 = None
delta_V = None

b0 = None
count = 0
mapper = vtk.vtkPolyDataMapper()
actor = vtk.vtkActor()
mesh = None
reader = vtk.vtkOBJReader()
renWin = vtk.vtkRenderWindow()


if __name__ == "__main__":
    coe_path = os.path.join("\\\\192.168.20.63\\ai\\Liyou_wang_data\\tf_output_v4", "coe.pkl")
    blendshape_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\Head_blendshapes"
    jpg_file = os.path.join("\\\\192.168.20.63\\ai\\Liyou_wang_data\\Texture", "head_D.jpg")
    model_path = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\Texture"
    name_file = "\\\\192.168.20.63\\ai\\Liyou_wang_data\\xiaoyueblendshapes\\names.pkl"
    names = load_pickle_file(name_file)
    number_blendshapes = len(names)
    coes = load_pickle_file(coe_path)
    v0, f0 = loadObj(os.path.join(blendshape_path, "head_geo.obj"))
    V = np.array(v0, dtype=np.float32).flatten()
    for name in names:
        if name != "head_geo":
            v, f = loadObj(os.path.join(blendshape_path, "{}.obj".format(name)))
            v = np.array(v, dtype=np.float32).flatten()
            V = np.vstack((V, v))
    V = np.delete(V, 0, axis=0)
    b0 = np.array(v0, dtype=np.float32).flatten()
    delta_V = V - b0

    ColorBackground = [0.0, 0.0, 0.0]
    model_name = os.path.join(model_path, "head_geo.obj")
    v, f = loadObj(model_name)
    reader = vtk.vtkOBJReader()
    reader.SetFileName(model_name)
    reader.Update()
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
    iren.CreateRepeatingTimer(0)
    iren.Start()