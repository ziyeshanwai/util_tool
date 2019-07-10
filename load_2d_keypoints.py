import json
import os
import numpy as np
import cv2


def GetJsonCorList(json_file):
    f = open(json_file, 'r')
    Frames_2d_keypoints = []
    for line in f.readlines():
        dic = json.loads(line)
        cor = dic['people'][0]["hand_right_keypoints_2d"]
        Frames_2d_keypoints.append(cor)
    f.close()
    return Frames_2d_keypoints


def get_Cordinate_2d(Frames_keypoints, i):
    frame = Frames_keypoints[i]
    Cordinates = []
    confidences = []
    for j in range(0, len(frame), 3):
        Cordinates.append([frame[j], frame[j + 1]])
        confidences.append(frame[j+2])
    Cors = np.array(Cordinates, dtype=np.float32)
    confiden = np.array(confidences, dtype=np.float32)
    return Cors, confiden


if __name__ == "__main__":
    json_file = os.path.join("../json_file", "2dkeypoints.json")
    Frames_2d_keypoints = GetJsonCorList(json_file)
    Cors, confiden = get_Cordinate(Frames_2d_keypoints, 542)
    print("Cors: {}".format(Cors))
    print("Confidence:{}".format(confiden))
    image_file = os.path.join("../image", "543.jpg")
    img = cv2.imread(image_file)
    for uv_points in Cors:
        cv2.circle(img, (uv_points[0], uv_points[1]), radius=2, color=(0, 0, 255), thickness=5)
    img = cv2.resize(img, (0, 0), fx=0.5, fy=0.5)
    cv2.namedWindow("test_2d_keypoints")
    cv2.imshow("test_2d_keypoints", img)
    cv2.waitKey(0)