from Util.util import *
import json
from itertools import chain


if __name__ == "__main__":
    json_file = "..\\json_file\\3dkeypoints.json"
    pkl_file = "..\\hand_output\\r_hand.pkl"
    write_file = "..\\json_file\\test_rhand.json"
    cor = None
    cor_list = load_pickle_file(pkl_file)
    # print(cor_list[2][0].tolist())

    f = open(json_file, 'r')
    Frames_keypoints = []
    i = 0
    with open(write_file, "w") as f_s:
        for line in f.readlines():
            dic = json.loads(line)
            ss = cor_list[i][0].tolist()
            cond = []
            for j in range(0, len(ss)):
                ss[j].append(1)
                cond.append(ss[j])
            dic['people'][0]["hand_right_keypoints_3d"] = list(chain.from_iterable(cond))
            json.dump(dic, f_s)
            f_s.write("\n")
            i += 1
        f.close()