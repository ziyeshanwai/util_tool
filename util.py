import os
import numpy as np
import pickle as pickle


def load_binary_pickle( filepath ):
    with open( filepath, 'rb' ) as f:
        data = pickle.load( f )
    return data


def save_binary_pickle( data, filepath ):
    with open( filepath, 'wb' ) as f:
        pickle.dump( data, f )

'''
加载简单的obj文件,只有顶点和边
v 1.5 6.3 3.5
...
f 1 2 3
f 4 5 6
这种
'''
def load_simple_obj(filename):
    f = open(filename, 'r')

    def get_num(string, type):
        if type == 'int':
            return int(string)
        elif type == 'float':
            return float(string)
        else:
            print('Wrong type specified')

    vertices = []
    faces = []

    for line in f:
        if '//' in line:
            str = line.split()
            len_str = len(str)
            for i in range(len_str):
                if '//' in str[i]:
                    str[i] = str[i].split('//')[0]
        else:
            str = line.split()
        if len(str) == 0:
            continue

        if str[0] == '#':
            continue
        elif str[0] == 'v':
            tmp_v = [get_num(s, 'float') for s in str[1:]]
            vertices.append( tmp_v )

        elif str[0] == 'f':
            tmp_f = [get_num(s, 'int')-1 for s in str[1:]]
            faces.append( tmp_f )

    f.close()
    return ( np.asarray(vertices), np.asarray(faces) )


def write_simple_obj( mesh_v, mesh_f, filepath, verbose=False ):
    with open( filepath, 'w') as fp:
        for v in mesh_v:
            fp.write( 'v %f %f %f\n' % ( v[0], v[1], v[2]) )
        for f in mesh_f+1: # Faces are 1-based, not 0-based in obj files
            fp.write( 'f %d %d %d\n' %  (f[0], f[1], f[2]) )
    if verbose:
        print('mesh saved to: ', filepath)


def safe_mkdir( file_dir ):
    if not os.path.exists( file_dir ):
        os.mkdir( file_dir ) 

