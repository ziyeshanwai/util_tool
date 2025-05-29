import bpy
import numpy as np

def main():
    obj = bpy.context.active_object
    head =  bpy.data.objects["GUYU_FaceMesh_LOD_0_uv_0"]
    curve_data = obj.data.curves
    curve_num = len(curve_data)
    diff_percent = 0.02
    # 检查属性是否存在
    if "surface_uv_coordinate" not in obj.data.attributes:
        print("找不到'surface_uv_coordinate'属性")
        return
    
#    attr = obj.data.attributes["surface_uv_coordinate"]
    curve_length_list = []
    uv_coor_list = []
    
    # 计算曲线长度和UV坐标
    for i, curve in enumerate(curve_data):
        point_num = curve.points_length
        start = curve.points[0].position
        end = curve.points[point_num-1].position
        curve_length = (end - start).length  # 使用Blender内置长度计算
#        uv = (attr.data[i].vector[0], attr.data[i].vector[1])
#        uv_coor_list.append(uv)
        curve_length_list.append(curve_length)
    
    # 打印全局长度统计
    print("\n===== 全局曲线长度统计 =====")
    print(f"平均长度: {np.mean(curve_length_list):.6f}")
    print(f"最大长度: {np.max(curve_length_list):.6f}")
    print(f"最小长度: {np.min(curve_length_list):.6f}")
    print(f"总曲线数: {len(curve_length_list)}")
    
    # 如果没有曲线，直接返回
    if not curve_length_list:
        print("没有找到有效曲线")
        return
    
    # 1. 按长度排序曲线
    sorted_indices = np.argsort(curve_length_list)
    sorted_lengths = np.array(curve_length_list)[sorted_indices]
    
    # 2. 基于均值阈值的滑动窗口聚类（10%差异）
    groups = []
    n = len(sorted_lengths)
    i = 0
    
    while i < n:
        # 初始化当前组
        current_indices = [sorted_indices[i]]
        current_lengths = [sorted_lengths[i]]
        
        # 尝试扩展组
        j = i + 1
        while j < n:
            # 临时添加下一个元素
            temp_lengths = current_lengths + [sorted_lengths[j]]
            temp_mean = np.mean(temp_lengths)
            temp_min = np.min(temp_lengths)
            temp_max = np.max(temp_lengths)
            
            # 检查最大/最小值与均值的差异是否≤10%
            max_diff = (temp_max - temp_mean) / temp_mean if temp_mean != 0 else 0
            min_diff = (temp_mean - temp_min) / temp_mean if temp_mean != 0 else 0
            
            if max_diff <= diff_percent and min_diff <= diff_percent:
                current_indices.append(sorted_indices[j])
                current_lengths = temp_lengths
                j += 1
            else:
                break  # 不满足条件则停止扩展
        
        # 添加当前组
        groups.append({
            "indices": current_indices,
            "lengths": current_lengths
        })
        
        i = j  # 移动到下一个未处理元素
    
    # 打印分组统计信息
    print("\n===== 分组统计信息 =====")
    for i, group in enumerate(groups):
        group_min = np.min(group["lengths"])
        group_max = np.max(group["lengths"])
        group_avg = np.mean(group["lengths"])
        group_range = group_max - group_min
        group_size = len(group["indices"])
        
        # 计算差异百分比
        max_diff_percent = 100 * (group_max - group_avg) / group_avg if group_avg > 0 else 0
        min_diff_percent = 100 * (group_avg - group_min) / group_avg if group_avg > 0 else 0
        
        print(f"Group_{i+1}:")
        print(f"  曲线数量: {group_size}")
        print(f"  长度范围: {group_min:.6f} - {group_max:.6f} (差值: {group_range:.6f})")
        print(f"  平均长度: {group_avg:.6f}")
        print(f"  最大值差异: {max_diff_percent:.2f}%")
        print(f"  最小值差异: {min_diff_percent:.2f}%")
    
    # 为每组创建新物体（使用网格）
    created_objects = []
    for i, group in enumerate(groups):
        indices = group["indices"]
        if not indices:
            print(f"\n跳过空组: Group_{i+1}")
            continue
        
        group_name = f"Group_{i+1}"
        
        # 创建新的网格数据
        mesh_data = bpy.data.meshes.new(f"{obj.name}_{group_name}_Mesh")
        
        # 准备顶点和边数据
        vertices = []
        edges = []
        vertex_index = 0
        
        # 遍历组内的每条曲线
        for curve_idx in indices:
            orig_curve = curve_data[curve_idx]
            
            # 添加顶点
            for point in orig_curve.points:
                vertices.append(point.position)
            
            # 添加边（连接曲线上的点）
            point_count = orig_curve.points_length
            edges.extend((vertex_index + k, vertex_index + k + 1) for k in range(point_count - 1))
            
            # 更新顶点索引
            vertex_index += point_count
        
        # 创建网格
        mesh_data.from_pydata(vertices, edges, [])
        mesh_data.update()
        
        # 创建新物体并添加到场景
        new_obj = bpy.data.objects.new(f"{obj.name}_{group_name}", mesh_data)
        new_obj.matrix_world = obj.matrix_world
        bpy.context.scene.collection.objects.link(new_obj)
        created_objects.append(new_obj)
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = new_obj
        new_obj.select_set(True)
        
        bpy.ops.object.convert(target='CURVE')
        bpy.ops.object.convert(target='CURVES')
        ob = bpy.context.active_object
        ob.data.surface = head
        ob.data.surface_uv_map = head.data.uv_layers[0].name
        bpy.ops.curves.convert_to_particle_system()
        head.particle_systems[new_obj.name].use_hair_dynamics = True
        if new_obj.name in bpy.data.objects:
            bpy.data.objects.remove(new_obj, do_unlink=True)


        
        print(f"\n创建 {group_name} 组物体:")
        print(f"  包含曲线: {len(indices)} 条")
        print(f"  顶点数量: {len(vertices)} 个")
        print(f"  平均长度: {np.mean(group['lengths']):.6f}")
    
    # 选择新创建的对象
    for obj in bpy.context.selected_objects:
        obj.select_set(False)
    for obj in created_objects:
        obj.select_set(True)
    if created_objects:
        bpy.context.view_layer.objects.active = created_objects[0]
        print(f"\n已选择 {len(created_objects)} 个新物体")

if __name__ == "__main__":
    main()
