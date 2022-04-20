import bpy
from scipy.spatial.transform import Rotation as R
import numpy as np



if __name__ == "__main__":
    c1 = bpy.data.objects["c1"]
    r = R.from_euler('x', -90, degrees=True)
    matrix =  r.as_matrix()
    print(matrix.dot(np.array(c1.location_world)))   
    rotation = matrix.dot(np.array(c1.rotation_euler.to_matrix()))
    r = R.from_matrix(rotation)
    print(r.as_quat())
    r = R.from_quat(test_quat)
    print(r.as_euler("xyz", degrees=True))