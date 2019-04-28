import PhotoScan
import csv
import os
import math

resultfolder = "\TemplatesPics"


def cross(a, b):
    result = PhotoScan.Vector([a.y*b.z - a.z*b.y, a.z*b.x - a.x*b.z, a.x*b.y - a.y *b.x])
    return result

def distance3d(p1,p2):
    distance = abs(math.sqrt((math.pow(p2[0]-p1[0],2))+(math.pow(p2[1]-p1[1],2))+(math.pow(p2[2]-p1[2],2))))
    return distance


def createMarker(marker_2D, nameiter):
    #camera = chunk.cameras[0]
    #marker_2D = (1666, 2690) #projections of marker on the given photo
    print('mk_2d', marker_2D)


    marker = chunk.addMarker()
    print('pj', marker.projections[camera])
    print('success')
    marker.projections[camera] = marker_2D

    point_2D = marker.projections[camera].coord
    vect = camera.sensor.calibration.unproject(point_2D)
    vect = camera.transform.mulv(vect)
    center = camera.center
    print(center)

    arr_points3D = []

    #estimating ray and surface intersection
    for face in model.faces:

        v = face.vertices

        E1 = PhotoScan.Vector(vertices[v[1]].coord - vertices[v[0]].coord)
        E2 = PhotoScan.Vector(vertices[v[2]].coord - vertices[v[0]].coord)
        D = PhotoScan.Vector(vect)
        T = PhotoScan.Vector(center - vertices[v[0]].coord)
        P = cross(D, E2)
        Q = cross(T, E1)
        result = PhotoScan.Vector([Q * E2, P * T, Q * D]) / (P * E1)

        if (0 < result[1]) and (0 < result[2]) and (result[1] + result[2] <= 1):
            t = (1 - result[1] - result[2]) * vertices[v[0]].coord
            u = result[1] * vertices[v[1]].coord
            v_ = result[2] * vertices[v[2]].coord

            point_3D = T0.mulp(u + v_ + t)

            if chunk.crs:
                point_3D = chunk.crs.project(point_3D)

            arr_points3D.append(point_3D)

            #break

    print (arr_points3D)

    arr_points = []
    for p in arr_points3D:
        if chunk.crs:
            point = chunk.crs.unproject(p)
        point = T0.inv().mulp(point)
        arr_points.append(point)

    # find nearest point
    finaldst = 99999
    index = 9999
    for i,pnt in enumerate(arr_points):
        dst = distance3d(center,pnt)
        if dst < finaldst:
            finaldst = dst
            index = i
    try:
        correct_pnt = arr_points[i]
    except UnboundLocalError:
        nameiter+=1
        return nameiter

    #print (arr_points)
    done = False


    markerlist = [marker]
    chunk.remove(markerlist)

    for c,cur_camera in enumerate(chunk.cameras):
        while not done:

            marker = chunk.addMarker()
            marker.label = "trackPoint_{0}".format(str(n))
            marker.projections[camera] = marker_2D

            cur_proj = cur_camera.project(correct_pnt)
            marker.projections[cur_camera] = cur_proj
            done = True

            nameiter += 1

    return nameiter

#read markers from file
def readMarkers(file):
    point_arr = []
    with open(file, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        for row in spamreader:
            point_arr.append((float(row[0]),float(row[1])))

    return point_arr

def readMarkers2():
    point_arr = []
    point_arr.append((float(1452), float(1672)))
    return point_arr


def dbg_test1():
    point2d = PhotoScan.Vector([1448, 1186])
    sensor = camera.sensor
    calibration = sensor.calibration
    p_x = camera.transform.mulp(sensor.calibration.unproject(point2d))
    print('p_x', p_x)
    print('camera center', camera.center)
    X = chunk.dense_cloud.pickPoint(camera.center, p_x)
    print('X', X)
    chunk.addMarker(point=X)


doc = PhotoScan.app.document
chunk = doc.chunk
model = chunk.model
vertices = chunk.model.vertices
T0 = chunk.transform.matrix
for ca in chunk.cameras:
    print('camera label: {}'.format(ca.label))
camera = chunk.cameras[6]   # camera index
print('*'*40)
print('camera label: {}'.format(camera.label))


n = 1

dbg_test1()


#markers = readMarkers(blah)
#markers = readMarkers2()

#for m in markers:
#    n = createMarker(m,n)


print("Script finished")
