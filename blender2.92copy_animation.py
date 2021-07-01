import bpy


def copy_animation(source_ob, target_ob):
    """
    source ob : origin source object 
    target ob : copy to target object
    """
    for i in range(bpy.context.scene.frame_start, bpy.context.scene.frame_end):
        bpy.context.scene.frame_set(i)
        for block in source_ob.data.shape_keys.key_blocks:
            if block.name != "Basis":
                target_ob.data.shape_keys.key_blocks[block.name].value=block.value
                target_ob.data.shape_keys.key_blocks[block.name].keyframe_insert("value", frame=i)
        if i % 10 == 0:
            print("copy frame {}".format(i))

if __name__ == "__main__":
    source_ani = "smooth_bs_ani"
    target_ani = "MetaHuman004"
    source_ob = bpy.data.objects[source_ani]
    target_ob = bpy.data.objects[target_ani]
    copy_animation(source_ob, target_ob)