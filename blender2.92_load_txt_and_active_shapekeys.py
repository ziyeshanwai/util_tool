import bpy


def loadbs(ob):
    file = r"E:\tempfile\bs.txt"
    with open(file, 'r') as f:
        lines = f.readlines()
        lines = [l.split(',')[0].split('.')[-1] for l in lines]
    
    for block in ob.data.shape_keys.key_blocks:
        if block.name == "Basis":
            continue
        if block.name.split("_")[-1] in lines:
            block.mute = False
        else:
            block.mute = True
            
            
def reset_mute(ob):
    for block in ob.data.shape_keys.key_blocks:
        block.mute = False
        
if __name__ == "__main__":
    
    ob = bpy.data.objects["fitv2"]
    loadbs(ob)
#    reset_mute(ob)