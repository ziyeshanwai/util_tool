from sklearn.decomposition import PCA
from Util.util import *


if __name__ == "__main__":
    face_model_path = "\\\\192.168.20.63\\ai\\face_data\\20190419\\Data_DeepLearning\\test_output"
    vert0, face0 = loadObj(os.path.join(face_model_path, "1.obj"))
    if not os.path.exists(os.path.join(face_model_path, "summary.npy")):
        verts = np.empty([len(vert0*3), 1], dtype=np.float32)
        for i in range(1, 9080):
            face_file = os.path.join(face_model_path, "{}.obj".format(i))
            if os.path.exists(face_file):
                vert, face = loadObj(face_file)
                vert = np.array(vert, dtype=np.float32).reshape([-1, 1])
                verts = np.hstack((verts, vert))
                if i % 100 == 0:
                    print("process {}...".format(i))
            else:
                print("{} is not existed".format(face_file))
        verts = np.delete(verts, 0, axis=1)
        np.save(os.path.join(face_model_path, "summary.npy"), verts)
        print("{} saved..".format(os.path.join(face_model_path, "summary.npy")))
    else:
        verts = np.load(os.path.join(face_model_path, "summary.npy"))
    verts_row_samples = verts.transpose()
    mean_value = np.mean(verts_row_samples, axis=0)
    verts_row_samples_mean = verts_row_samples - mean_value
    pca = PCA(n_components=160, whiten=False)
    pca.fit(verts_row_samples)
    data_reduced = pca.transform(verts_row_samples)
    print(data_reduced.shape)
    print("coe is {}".format(data_reduced.shape))
    print("特征向量的维度是{}".format(pca.components_.shape))
    writeObj(os.path.join("./Blendshapes", "{}.obj".format("mean_value")), mean_value.reshape([-1, 3]).tolist(), face0)
    for i in range(0, 160):
        feature_vector = pca.components_[i, :] + mean_value
        v = np.reshape(feature_vector, [-1, 3])
        writeObj(os.path.join("./Blendshapes", "{}.obj".format(i)), v.tolist(), face0)