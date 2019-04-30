# coding: = utf-8
# Author: Liyou

from sklearn.decomposition import PCA
from util import *
"""
实际训练的数据应该仅仅是平滑后面部数据
对面部数据做一次PCA，观察每一个特征向量样子，特征值理论上即为blendshape系数
变化这些系数，看是叠加后的数据如何变化
如果数据的单位是一致的，注意使用PCA时不要对每个维度归一化，不同的归一化方式会对
PCA结果产生较大影响，在本文人脸中需要归一化，在将特征变量变回原始数据的表达形式时，
要加均值
PCA是像最大方差的方向做投影，如果数据归一化了，那么各个维度间的差距会变小，导致主成分提取不好
"""
colorMaps = ["Reds", "Oranges", "Purples", "Accent", "black-white", "blue-red",
             "Blues", "bone", "Greens", "Greys", "purples"]


if __name__ == "__main__":
    face_model_path = "\\\\192.168.80.195\data3\LiyouWang\smooth_curve_face"
    vert0, face0 = loadObj(os.path.join(face_model_path, "0.obj"))
    if not os.path.exists(os.path.join(face_model_path, "summary.npy")):
        verts = np.empty([len(vert0*3), 1], dtype=np.float32)
        for i in range(0, 500):
            face_file = os.path.join(face_model_path, "{}.obj".format(i))
            if os.path.exists(face_file):
                vert, face = loadObj(face_file)
                vert = np.array(vert, dtype=np.float32).reshape([-1, 1])
                verts = np.hstack((verts, vert))
                if i % 100 == 0:
                    print("process {}...".format(i))
            else:
                print("{} is not existed".format(face_file))
        np.save(os.path.join(face_model_path, "summary.npy"), verts)
        print("{} saved..".format(os.path.join(face_model_path, "summary.npy")))
    else:
        verts = np.load(os.path.join(face_model_path, "summary.npy"))
        verts_row_samples = verts.transpose()
        mean_value = np.mean(verts_row_samples, axis=0)
        verts_row_samples_mean = verts_row_samples - mean_value
        var_value = np.var(verts_row_samples, axis=0)
        data = verts_row_samples_mean/var_value
        print("verts_row_samples_mean shape is {}".format(mean_value.shape))
        print("verts_row_samples_std shape is {}".format(var_value.shape))
        pca = PCA(n_components=0.99998, whiten=False)
        pca.fit(verts_row_samples)
        print("components_ shape is {}".format(pca.components_.shape))
        # feature_vector = coe.dot(pca.components_) + mean_value
        writeObj(os.path.join("./Models", "{}.obj".format("mean_value")), mean_value.reshape([-1, 3]).tolist(), face0)
        for i in range(0, 10):
            feature_vector = pca.components_[i, :] # + mean_value
            v = np.reshape(feature_vector, [-1, 3])
            writeObj(os.path.join("./Models", "{}.obj".format(i)), v.tolist(), face0)
            # print(np.dot(pca.components_[i, :], pca.components_[i+1, :].T))


