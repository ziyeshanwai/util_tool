import os
import cv2


if __name__ == "__main__":

    images_path = r"\\192.168.20.63\ai\Liyou_wang_data\double_cameras_video\imgs\xy1\18286112_rot_optical_flow"
    fps = 30    # 保存视频的FPS，可以适当调整
    # 可以用(*'DVIX')或(*'X264'),如果都不行先装ffmepg: sudo apt-get install ffmepg
    # fourcc = cv2.VideoWriter_fourcc(*'DVIX')
    videoWriter = cv2.VideoWriter('moon.mp4', cv2.CAP_OPENCV_MJPEG, fps, (512, 640), False)  # 最后一个是保存图片的尺寸

    for i in range(0, 5266):
        img = cv2.imread(os.path.join(images_path, "{}.jpg".format(i)))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        img = img.T  # 取决于图片是不是倒着的
        img = cv2.flip(img, 1)  # 需要做一次对称
        frame = cv2.resize(img, dsize=(258, 386))
        videoWriter.write(frame)
        print("process {}".format(i))
    videoWriter.release()
