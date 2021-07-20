from __future__ import print_function
import bpy
import os


D = bpy.data

outputFolder= r"E:\blender_tmp_file"

printFrameNums = True # include frame numbers in the csv file
relativeCoords = False # marker coords will be relative to the dimensions of the clip

f2=open(os.path.join(outputFolder, 'export-markers.log'), 'w')
print('First line test', file=f2)
for clip in D.movieclips:
    print('clip {0} found\n'.format(clip.name), file=f2)
    width=clip.size[0]
    height=clip.size[1]
    for ob in clip.tracking.objects:
        print('object {0} found\n'.format(ob.name), file=f2)
        for track in ob.tracks:
            print('track {0} found\n'.format(track.name), file=f2)
            fn = os.path.join(outputFolder,'{0}_{1}_tr_{2}.csv'.format(clip.name.split('.')[0], ob.name, track.name))
            with open(fn, 'w') as f:
                framenum = 0
                while framenum < clip.frame_duration:
                    markerAtFrame = track.markers.find_frame(framenum)
                    if markerAtFrame:
                        coords = markerAtFrame.co.xy
                        if relativeCoords:
                            if printFrameNums:
                                print('{0},{1},{2}'.format(framenum, coords[0], coords[1]), file=f)
                            else:
                                print('{0},{1}'.format(coords[0], coords[1]), file=f)
                        else:
                            if printFrameNums:
                                print('{0},{1},{2}'.format(framenum, coords[0]*width, coords[1]*height), file=f)
                            else:
                                print('{0},{1}'.format(coords[0]*width, coords[1]*height), file=f)

                    framenum += 1
f2.close()