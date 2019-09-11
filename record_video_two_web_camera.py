import cv2
import time
import numpy as np


if __name__ == "__main__":
    width = int(1280)  # 960 540 1920 1080 1280 720
    height = int(720)
    cap_left = cv2.VideoCapture(1)  # 调整左右
    cap_left.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap_left.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    cap_right = cv2.VideoCapture(0)
    cap_right.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    cap_right.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out_left = cv2.VideoWriter('./output/output_left.avi', fourcc, 15.0, (width, height))
    out_right = cv2.VideoWriter('./output/output_right.avi', fourcc, 15.0, (width, height))
    recording = False
    cv2.namedWindow("capture_left", cv2.WND_PROP_FULLSCREEN)
    cv2.resizeWindow("capture_left", 360, 720)
    cv2.namedWindow("capture_right", cv2.WND_PROP_FULLSCREEN)
    cv2.resizeWindow("capture_right", 360, 720)
    while True:
        # get a frame
        start = time.time()
        ret_left, frame_left = cap_left.read()
        ret_right, frame_right = cap_right.read()
        end = time.time()
        # show a frame
        # im_left_show = frame_left
        # im_right_show = frame_right
        # im_left_show = cv2.transpose(cv2.resize(frame_left, (0, 0), fx=0.5, fy=0.5))
        # im_right_show = cv2.transpose(cv2.resize(frame_right, (0, 0), fx=0.5, fy=0.5))
        im_left_show = np.rot90(frame_left, 1)
        im_right_show = np.rot90(frame_right, 1)
        # cv2.imshow("capture_left", cv2.flip(im_left_show, 0))
        # cv2.imshow("capture_right", cv2.flip(im_right_show, 0))
        cv2.imshow("capture_left", im_left_show)
        cv2.imshow("capture_right", im_right_show)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            recording = True
            print("start recording")
        elif key & 0xFF == ord('q'):
            print("break")
            break
        if recording:
            out_left.write(frame_left)
            out_right.write(frame_right)
            end = time.time()
            print("time is {}".format(end - start))

    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()