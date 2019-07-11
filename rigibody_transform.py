import numpy as np
import math
from scipy.optimize import least_squares
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from scipy.spatial.transform import Rotation
import cv2


def R_to_axis_angle(matrix):
    """Convert the rotation matrix into the axis-angle notation.
    Conversion equations
    ====================
    From Wikipedia (http://en.wikipedia.org/wiki/Rotation_matrix), the conversion is given by::
        x = Qzy-Qyz
        y = Qxz-Qzx
        z = Qyx-Qxy
        r = hypot(x,hypot(y,z))
        t = Qxx+Qyy+Qzz
        theta = atan2(r,t-1)
    @param matrix:  The 3x3 rotation matrix to update.
    @type matrix:   3x3 numpy array
    @return:    The 3D rotation axis and angle.
    @rtype:     numpy 3D rank-1 array, float
    """
    # Axes.
    axis = np.zeros(3, np.float64)
    axis[0] = matrix[2, 1] - matrix[1, 2]
    axis[1] = matrix[0, 2] - matrix[2, 0]
    axis[2] = matrix[1, 0] - matrix[0, 1]
    # Angle.
    r = np.hypot(axis[0], np.hypot(axis[1], axis[2]))
    t = matrix[0, 0] + matrix[1, 1] + matrix[2, 2]
    theta = math.atan2(r, t - 1)
    # Normalise the axis.
    axis = axis / r
    # Return the data.
    return axis, theta


def R_axis_angle(matrix, axis, angle):
    """Generate the rotation matrix from the axis-angle notation.
    Conversion equations
    ====================
    From Wikipedia (http://en.wikipedia.org/wiki/Rotation_matrix), the conversion is given by::
        c = cos(angle); s = sin(angle); C = 1-c
        xs = x*s;   ys = y*s;   zs = z*s
        xC = x*C;   yC = y*C;   zC = z*C
        xyC = x*yC; yzC = y*zC; zxC = z*xC
        [ x*xC+c   xyC-zs   zxC+ys ]
        [ xyC+zs   y*yC+c   yzC-xs ]
        [ zxC-ys   yzC+xs   z*zC+c ]
    @param matrix:  The 3x3 rotation matrix to update.
    @type matrix:   3x3 numpy array
    @param axis:    The 3D rotation axis.
    @type axis:     numpy array, len 3
    @param angle:   The rotation angle.
    @type angle:    float
    """
    # Trig factors.
    ca = np.cos(angle)
    sa = np.sin(angle)
    C = 1 - ca
    # Depack the axis.
    x, y, z = axis
    # Multiplications (to remove duplicate calculations).
    xs = x*sa
    ys = y*sa
    zs = z*sa
    xC = x*C
    yC = y*C
    zC = z*C
    xyC = x*yC
    yzC = y*zC
    zxC = z*xC
    # Update the rotation matrix.
    matrix[0, 0] = x*xC + ca
    matrix[0, 1] = xyC - zs
    matrix[0, 2] = zxC + ys
    matrix[1, 0] = xyC + zs
    matrix[1, 1] = y*yC + ca
    matrix[1, 2] = yzC - xs
    matrix[2, 0] = zxC - ys
    matrix[2, 1] = yzC + xs
    matrix[2, 2] = z*zC + ca
    return matrix


def resSimXform(b, A, B):
    t = b[4:7]
    R = np.zeros((3, 3))
    R = R_axis_angle(R, b[0:3], b[3])
    rot_A = b[7]*R.dot(A) + t[:, np.newaxis]
    result = np.sqrt(np.sum((B-rot_A)**2, axis=0))
    return result


"""
method 1
"""
def caculate_transform(Model, Data):
    """
    使用此方法要求点数大于等于8
    calculate the R t s between PointsA and PointsB
    :param Model: n * 3  ndarray
    :param Data: n * 3  ndarray
    :return: R t s
    """

    model = Model.T  # 3 * n
    data = Data.T  # 3 * n
    cent = np.vstack((np.mean(model, axis=1), np.mean(data, axis=1))).T
    cent_0 = cent[:, 0]
    model_center = cent_0[:, np.newaxis]
    cent_1 = cent[:, 1]
    data_center = cent_1[:, np.newaxis]
    model_zerocentered = model - model_center
    data_zerocentered = data - data_center
    n = model.shape[1]
    Cov_matrix = 1.0/n * model_zerocentered.dot(data_zerocentered.T)
    U, D, V = np.linalg.svd(Cov_matrix)
    V = V.T
    W = np.eye(V.shape[0], V.shape[0])
    if np.linalg.det(V.dot(W).dot(U.T)) == -1:
        print("计算出的旋转矩阵为反射矩阵，纠正中..")
        W[-1, -1] = np.linalg.det(V.dot(U.T))
    R = V.dot(W).dot(U.T)
    sigma2 = (1.0 / n) * np.multiply(data_zerocentered, data_zerocentered).sum()
    s = 1.0 / sigma2 * np.trace(np.dot(np.diag(D), W))
    t = model_center - s*R.dot(data_center)
    b0 = np.zeros((8,))
    if np.isreal(R).all():
        axis, theta = R_to_axis_angle(R)
        b0[0:3] = axis
        b0[3] = theta
        if not np.isreal(b0).all():
            b0 = np.abs(b0)
    else:
        print("R is {}".format(R))
        print("R中存在非实数")
    b0[4:7] = t.T
    b0[7] = s
    b = least_squares(fun=resSimXform, x0=b0, jac='2-point', method='lm', args=(data, model),
                      ftol=1e-12, xtol=1e-12, gtol=1e-12, max_nfev=100000)  # 参数只能是一维向量么
    r = b.x[0:4]
    t = b.x[4:7]
    s = b.x[7]
    R = R_axis_angle(R, r[0:3], r[3])
    rot_A = s*R.dot(data) + t[:, np.newaxis]
    res = np.sum(np.sqrt(np.sum((model-rot_A)**2, axis=1)))/model.shape[1]
    print("对齐误差是{}".format(res))
    return R, t, s


"""
method 2
"""
def align_sim3(model, data):
  """Implementation of the paper: S. Umeyama, Least-Squares Estimation
  of Transformation Parameters Between Two Point Patterns,
  IEEE Trans. Pattern Anal. Mach. Intell., vol. 13, no. 4, 1991.

  Input:
  model -- first trajectory (3xn)
  data -- second trajectory (3xn)

  Output:
  s -- scale factor (scalar)
  R -- rotation matrix (3x3)
  t -- translation vector (3x1)
  t_error -- translational error per point (1xn)

  """

  # substract mean
  mu_M = model.mean(axis=1).reshape(model.shape[0], 1)
  mu_D = data.mean(axis=1).reshape(data.shape[0], 1)
  model_zerocentered = model - mu_M
  data_zerocentered = data - mu_D
  n = np.shape(model)[1]

  # correlation
  data_zerocentered_T = np.transpose(data_zerocentered)
  C = 1.0/n*np.dot(model_zerocentered, data_zerocentered_T)
  # print("data_zerocentered is {}".format(data_zerocentered))
  sigma2 = 1.0/n*np.multiply(data_zerocentered, data_zerocentered).sum()  # np.multiply element-wise multiply
  print("sigma2 is {}".format(sigma2))
  U_svd, D_svd, V_svd = np.linalg.linalg.svd(C)
  D_svd = np.diag(D_svd)
  V_svd = np.transpose(V_svd)  # 为什么转置
  S = np.eye(3)

  if(np.linalg.det(U_svd)*np.linalg.det(V_svd) < 0):  # 防止是反射矩阵
    print("反射矩阵")
    S[2, 2] = -1

  R = np.dot(U_svd, np.dot(S, np.transpose(V_svd)))
  s = 1.0/sigma2 * np.trace(np.dot(D_svd, S))
  t = mu_M - s * np.dot(R, mu_D)

  # TODO:
  model_aligned = s * R.dot(data) + t
  # alignment_error = model_aligned - model
  # t_error = np.sum(np.sqrt(np.sum(np.multiply(alignment_error, alignment_error), 0)))/model.shape[1]  # matrix.A 矩阵
  t_error = np.sum(np.sqrt(np.sum((model - model_aligned) ** 2, axis=1))) / model.shape[1]
  print("对齐误差是{}".format(t_error))
  return s, R, t, t_error


def Create_Rotation_Matrix(vecA, vecB):
    """
    由A方向转向B方向
    :param vecA: [3, 1] numpy
    :param vecB: [3, 1]
    :return: 旋转矩阵
    """
    sita = math.acos(vecA.dot(vecB.T)/(np.linalg.norm(vecA)*np.linalg.norm(vecB)))
    ro_vector = vecA / np.linalg.norm(vecA) * np.abs(sita)
    R = cv2.Rodrigues(ro_vector)
    return R[0]


if __name__ == "__main__":

    n = 8
    R = Create_Rotation_Matrix(np.random.rand(1, 3)*20, np.random.rand(1, 3)*10)
    t = np.random.rand(1, 3) * 100
    s = 10
    print("R is {}".format(R))
    print("t is {}".format(t))
    print("s is {}".format(s))
    PA = np.random.rand(n, 3)
    PB = s*PA.dot(R) + t
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(PA[:, 0], PA[:, 1], PA[:, 2], color='red')
    ax.scatter(PB[:, 0], PB[:, 1], PB[:, 2], color='yellow')
    plt.show()
    print("---------------------------")
    print("using method 1")
    # print("PB is {}".format(PB))
    RR, tt, ss = caculate_transform(PB, PA)
    print("RR is {}".format(RR))
    print("tt is {}".format(tt))
    print("ss is {}".format(ss))
    # print("PB_hat is {}".format(ss*PA.dot(RR) + tt))
    print("------------------------")
    print("using method 2")
    "method 2"
    s, R, t, t_error = align_sim3(PB.T, PA.T)
    print("RR is {}".format(R))
    print("tt is {}".format(t))
    print("s is {}".format(s))
