import bpy

def clear_hair_particles():
    # 遍历场景中的所有物体
    for obj in bpy.context.scene.objects:
        # 仅处理存在粒子系统的物体
        if obj.particle_systems:
            # 反向遍历粒子系统索引（避免移除后索引错位）
            for index in reversed(range(len(obj.particle_systems))):
                ps = obj.particle_systems[index]
                # 检查粒子类型是否为毛发（HAIR）
                if ps.settings.type == 'HAIR':
                    # 通过索引移除粒子系统（关键修正：使用 pop 替代 remove）
                    bpy.ops.object.particle_system_remove()



if __name__ == "__main__":
    clear_hair_particles()
    print("所有毛发粒子系统清除完成")
    
