import bpy
import numpy as np
import os
import mathutils
from scipy.optimize import nnls


def get_marker_position(clip_name, frame):
    """
    get frame coordinate in pixle
    """
    track_data = bpy.data.movieclips[clip_name].tracking
    clip_width = bpy.data.movieclips[clip_name].size[0]
    clip_height = bpy.data.movieclips[clip_name].size[1]
    pix_coor = []
    ind = []
    coor_arr = []
    for t in track_data.tracks:
        x = t.markers.find_frame(frame).co.xy[0] * clip_width
        y = (1 - t.markers.find_frame(frame).co.xy[1]) * clip_height
        pix_coor.append({t.name:(x, y)})
        coor_arr.append([x, y])
        ind.append(t.name)

    return np.array(coor_arr), ind


def get_specified_name_marker_position(clip_name, frame, name):
    track_data = bpy.data.movieclips[clip_name].tracking
    clip_width = bpy.data.movieclips[clip_name].size[0]
    clip_height = bpy.data.movieclips[clip_name].size[1]
    if track_data.tracks[name].markers.find_frame(frame) == None:
        return None
    else:   
        x = track_data.tracks[name].markers.find_frame(frame).co.xy[0] * clip_width
        y = (1 - track_data.tracks[name].markers.find_frame(frame).co.xy[1]) * clip_height
        return [x, y]
    

def get_all_markers(clip_name):
    track_data = bpy.data.movieclips[clip_name].tracking
    clip_width = bpy.data.movieclips[clip_name].size[0]
    clip_height = bpy.data.movieclips[clip_name].size[1]
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    els = [get_specified_name_marker_position(clip_name, i, "el") for i in range(start_frame, end_frame + 1)]
    ers = [get_specified_name_marker_position(clip_name, i, "er") for i in range(start_frame, end_frame + 1)]
    roots = [get_specified_name_marker_position(clip_name, i, "track_root") for i in range(start_frame, end_frame + 1)]
    return els, ers, roots


def initial_tracks(clip_name):
    track_data = bpy.data.movieclips[clip_name].tracking
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    last_co = None
    for t in track_data.tracks:
        for frame in range(start_frame, end_frame + 1):
            if t.markers.find_frame(frame):
                last_co = t.markers.find_frame(frame).co
            else:
                print("insert frame {}".format(frame))
                t.markers.insert_frame(frame=frame, co=last_co)
                
                
def delete_specified_name_frame(clip_name, frame, name):
    track_data = bpy.data.movieclips[clip_name].tracking
    track_data.tracks[name].markers.delete_frame(frame)
     

def map_tracking_data2_controller(clip_name, keyframes):
    locations = []
    els = []
    ers = []
    e_roots = []
    """
    get sample
    """
    for k in keyframes:
        bpy.context.scene.frame_set(k)  # !!! is different from frame_current should only really be used as a read-only property
        loc = bpy.data.objects["Armature"].pose.bones["eye_controller"].location
        el = get_specified_name_marker_position(clip_name, k, "el")
        er = get_specified_name_marker_position(clip_name, k, "er")
        root = get_specified_name_marker_position(clip_name, k, "track_root")
        if el and er and root:
            els.append(el)
            ers.append(er)
            e_roots.append(root)
            locations.append(np.array(loc).tolist())
    location_sample_np = np.array(locations).T 
    el_samples = np.array(els) - np.array(e_roots)
    er_samples = np.array(ers) - np.array(e_roots)
    A = np.hstack((el_samples, er_samples)).T
    start_frame = bpy.context.scene.frame_start
    end_frame = bpy.context.scene.frame_end
    for f in range(start_frame, end_frame + 1):  
        print("calculat frame {}".format(f))
        el = get_specified_name_marker_position(clip_name, f, "el")
        er = get_specified_name_marker_position(clip_name, f, "er")
        e_root = get_specified_name_marker_position(clip_name, f, "track_root")
        if el and er and root:
            eld = np.array(el) - np.array(e_root)
            erd = np.array(er) - np.array(e_root)
            b = np.hstack((eld, erd))
            weights, _ = nnls(A, b)
            weights, residuals, rnk, s = np.linalg.lstsq(A, b)
            print("weights is {}".format(weights))
            new_location = location_sample_np.dot(weights[:, np.newaxis])
            bpy.context.scene.frame_set(f)
            bpy.data.objects["Armature"].pose.bones["eye_controller"].location = mathutils.Vector((new_location[0], new_location[1], new_location[2]))
            bpy.data.objects["Armature"].pose.bones["eye_controller"].keyframe_insert("location", frame=f)
        else:
            continue
        

if __name__ == "__main__":
    clip_name = 'yourvideo.mp4'
    keyframes = [1, 510, 1178, 1268, 1302, 1365, 1477, 4953, 5347, 5676]
    map_tracking_data2_controller(clip_name, keyframes)
    