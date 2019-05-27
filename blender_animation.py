import bpy
from mathutils import Vector
import bmesh
import numpy as np
import os


def loadObj(path):
    if path.endswith('.obj'):
        f = open(path, 'r')
        lines = f.readlines()
        vertics = []
        faces = []
        vts = []
        for line in lines:
            if line.startswith('v') and not line.startswith('vt') and not line.startswith('vn'):
                line_split = line.split()
                ver = line_split[1:4]
                ver = [float(v) for v in ver]
                vertics.append(ver)
            else:
                if line.startswith('f'):
                    line_split = line.split()
                    if '/' in line: 
                        tmp_faces = line_split[1:]
                        f = []
                        for tmp_face in tmp_faces:
                            f.append(int(tmp_face.split('/')[0]))
                        faces.append(f)
                    else:
                        face = line_split[1:]
                        face = [int(fa) for fa in face]
                        faces.append(face)
        return (vertics, faces)


frames = 5
bpy.context.scene.frame_start = 0
bpy.context.scene.frame_end = frames
model_path = "\\\\192.168.80.195\\data3\\LiyouWang\\uv_objs"
bpy.data.window_managers["WinMan"].key_points = True
for i in range(0, frames):
    if os.path.exists(os.path.join(model_path, "smooth-{}.obj".format(i))):
        bpy.context.scene.frame_set(i)
        v, f = loadObj(os.path.join(model_path, "smooth-{}.obj".format(i)))
        verts = np.array(v, dtype=np.float32)
        verts = np.reshape(verts, [-1, ])
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.context.object.data.vertices.foreach_set("co", verts)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.anim.insert_keyframe_animall()
        print("the {} is inserted".format(i))