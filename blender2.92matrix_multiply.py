# matrix world @ co convert to numpy mulatiply
import numpy as np
import bpy


if __name__ == "__main__":
    ob = bpy.data.objects["Object000"]
    world_matrix = ob.matrix_world
    v = ob.data.vertices[100].co
    world_matrix_np = np.array(world_matrix)
    v_np = np.array(v).reshape(-1, 3)
    v_np_4d = np.ones((v_np.shape[0], 4), dtype=np.float32)
    v_np_4d[:, :-1] = v_np
    print(world_matrix_np.shape)
    print(v_np.shape)
    gt = world_matrix @ v
    gt_numpy = np.einsum('ij,aj->ai', world_matrix_np, v_np_4d)[:, :-1]
    print("v np 4d shape is {}".format(v_np_4d.shape))
    print(world_matrix_np.dot(v_np_4d.T))
    print("gt is {}".format(gt))
    print("gt numpy is {}".format(gt_numpy))
    #assert gt == gt_numpy, "matrix @ vector is not equal matrix dot numpy format"