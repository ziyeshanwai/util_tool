# Author:liyou Wang
# Date:2019.1.28
# description:检测两个mesh是否拓扑一致,即:点数一致和边一致
from util import load_simple_obj
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np


class Obj(object):
    '''
    存储顶点和边,顶点和边均为numpy数组
    '''
    def __init__(self, v, f):
        self.vertex = v
        self.edges = f


def judgetoposame(obj1, obj2):
    v1 = obj1.vertex
    v2 = obj2.vertex
    f1 = obj1.edges
    f2 = obj2.edges
    if v1.size == v2.size:
        fig1 = plt.figure()
        ax1 = Axes3D(fig1)
        tmp = np.random.randint(low=0, high=int(v1.size/3), size=int(v1.size/20), dtype=np.int32)
        ax1.scatter(v1[tmp, 0], v1[tmp, 1], v1[tmp, 2], color='red')
        fig2 = plt.figure()
        ax2 = Axes3D(fig2)
        ax2.scatter(v1[tmp, 0], v1[tmp, 1], v1[tmp, 2], color='blue')
        print(f1-f2)
        return (f1 == f2).all()
    else:
        return False


def main(obj1_path, obj2_path):
    v, f = load_simple_obj(obj1_path)
    obj1 = Obj(v, f)
    v, f = load_simple_obj(obj2_path)
    obj2 = Obj(v, f)
    return judgetoposame(obj1, obj2)


if __name__ == '__main__':
    obj1_path = 'D:\\Deformation-Transfer-Matlab-master\\Dingyuan.obj'
    obj2_path = 'D:\\Deformation-Transfer-Matlab-master\\Huling.obj'
    print('the {} and {} topology same is {}'.format(obj1_path, obj2_path, main(obj1_path, obj2_path)))
    plt.show()