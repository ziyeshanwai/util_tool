import bpy
import numpy as np
import os


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
     


if __name__ == "__main__":
    clip_name = 'your_video.mp4'
    initial_tracks(clip_name)
    els, ers, roots = get_all_markers(clip_name)
    print(len(els))
    print(len(ers))
    print(len(roots))
    