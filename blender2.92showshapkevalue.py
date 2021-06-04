import bpy
import os
import json

def export_metahuman_json(ob, outputpath):
    
    """
    export metahuman curve to json
    export the selected frame start frame end curve
    """
    dict_ani = {}
    for block in ob.data.shape_keys.key_blocks:
        if block.name != "Basis":
            dict_ani[block.name] = []
            if block.name == "CTRL_expressions_jawChinRaiseDL":
                for i in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
                    bpy.context.scene.frame_current = i
                    bpy.context.view_layer.update() # important
                    tmp = {}
                    tmp["frameNum"] = i
                    tmp["value"] = block.value
    #                dict_ani[block.name].append(tmp)
                    
                    print("block : {}, tmp:{}".format(block, tmp))
    print("export over!")

def export_metahuman_json2(ob, outputpath):
    
    """
    export metahuman curve to json
    export the selected frame start frame end curve
    """
    dict_channel = {}
    for i in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
        bpy.context.scene.frame_set(i)
        for block in ob.data.shape_keys.key_blocks:
            if block.name != "Basis":
                tmp = {}
                tmp["frameNum"] = i
                tmp['value'] = block.value
                if block.name in dict_channel.keys():
                    dict_channel[block.name].append(tmp)
                else:
                    dict_channel[block.name] = []
        print("export {}".format(i))
#    print("export over!")
    write_json(outputpath, dict_channel)



if __name__ == "__main__":
   ob = bpy.data.objects['head_geo']
   outputpath = r""
   export_metahuman_json(ob, outputpath)