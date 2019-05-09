# -*- coding: utf-8 -*-
import wrap
from wrap import Geom
import os
import json

def load_json(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def write_json(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def main(geom_path, src, dist):
    if not os.path.exists(geom_path):
        print('%s not found' % geom_path)
        return
    if not os.path.exists(src):
        print('%s not found' % src)
        return
    geom = wrap.Geom(geom_path)
    
    triangles = load_json(src)
    points = []
    shows = []
    for triangle in triangles:
        wp = wrap.PointOnTriangle(*triangle)
        (x,y,z) = geom.pointOnTriangleToPoint(wp)
        points.append([round(x, 8), round(y, 8), round(z, 8)])
        shows.append(wp)

    print(points)
    write_json(dist, points)
    
    wrap.selectPoints(geom, None, shows)

if __name__ == '__main__':
#    main(
#        "D:\\Blendshape-Based Animation\\triangemesh-source\\xiaoyue.0013.obj",
#        "D:\\Blendshape-Based Animation\\triangemesh-source\\source.txt",
#        "D:\\Blendshape-Based Animation\\triangemesh-source\\neural-source-points.txt"
#    )
#    main(
#        "D:\\Blendshape-Based Animation\\charactor\\Xiaoyue_tri.obj",
#        "D:\\Blendshape-Based Animation\\charactor\\target.txt",
#        "D:\\Blendshape-Based Animation\\charactor\\neural-target-points.txt"
#    )
#    main(
#        "D:\\Blendshape-Based Animation\\charactor_quads\\xiaoyue.0013.obj",
#        "D:\\Blendshape-Based Animation\\charactor_quads\\2correct_points.txt",
#        "D:\\Blendshape-Based Animation\\charactor_quads\\corrct3D-points.txt"
#    )
#    main(
#        "D:\\FaceExpressionTransfer\\Models\\p1\\Source\\neural_pose\\base.obj",
#        "D:\\FaceExpressionTransfer\\Models\\p1\\Source\\txt\\source.txt",
#        "D:\\FaceExpressionTransfer\\Models\\p1\\Source\\txt\\neural-source-points.txt"
#    )
#    main(
#        "D:\\FaceExpressionTransfer\\Models\\p1\\Target\\Head\\Xiaoyue_quad.obj",
#        "D:\\FaceExpressionTransfer\\Models\\p1\\Target\\txt\\target.txt",
#        "D:\\FaceExpressionTransfer\\Models\\p1\\Target\\txt\\neural-target-points.txt"
#    )
    main(
        "\\\\192.168.80.195\\data3\\LiyouWang\\baseFace\\0.obj",
        "\\\\192.168.80.195\\data3\\LiyouWang\\baseFace\\source.txt",
        "\\\\192.168.80.195\\data3\\LiyouWang\\baseFace\\neural-source-points.txt"
    )
    
  
