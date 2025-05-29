import bpy
import numpy as np

def main():
    # 用户设置：在这里修改分组数量
    NUM_GROUPS = 20 # 修改这个值来改变分组数量
    
    obj = bpy.context.active_object
    curve_data = obj.data.curves
    curve_num = len(curve_data)
#    attr = obj.data.curves.data.attributes["surface_uv_coordinate"]
    curve_length_list = []
    uv_coor_list = []
    
    # 保留原始代码（计算曲线长度和UV坐标）
    for i, curve in enumerate(curve_data):
        point_num = curve.points_length
        start = curve.points[0].position
        end = curve.points[point_num-1].position
        curve_length = np.linalg.norm(end-start)
#        uv = (attr.data[i].vector[0], attr.data[i].vector[1])
#        uv_coor_list.append(uv)
        curve_length_list.append(curve_length)
    
    # 保留原始代码（打印长度统计）
    print("\n===== 全局曲线长度统计 =====")
    print(f"平均长度: {np.mean(curve_length_list):.6f}")
    print(f"最大长度: {np.max(curve_length_list):.6f}")
    print(f"最小长度: {np.min(curve_length_list):.6f}")
    print(f"总曲线数: {len(curve_length_list)}")
    
    # 保留原始代码（获取头部和UV映射）
    head = obj.data.surface
    UVMap = obj.data.surface_uv_map
    
    # 如果没有曲线，直接返回
    if not curve_length_list:
        print("没有找到有效曲线")
        return
    
    # 根据分组数量创建分组
    sorted_lengths = sorted(curve_length_list)
    group_thresholds = []
    
    # 计算分组阈值
    for i in range(1, NUM_GROUPS):
        threshold_index = int(len(sorted_lengths) * i / NUM_GROUPS)
        if threshold_index < len(sorted_lengths):
            group_thresholds.append(sorted_lengths[threshold_index])
    
    # 创建分组字典（包含长度数据）
    groups = {}
    for i in range(NUM_GROUPS):
        group_name = f"Group_{i+1}"
        groups[group_name] = {
            "indices": [],
            "lengths": []
        }
    
    # 分配曲线到对应分组
    for i, length in enumerate(curve_length_list):
        group_index = 0
        # 找到曲线所属的分组
        while group_index < len(group_thresholds) and length > group_thresholds[group_index]:
            group_index += 1
        
        group_name = f"Group_{group_index+1}"
        groups[group_name]["indices"].append(i)
        groups[group_name]["lengths"].append(length)
    
    # 打印分组统计信息
    print("\n===== 分组统计信息 =====")
    for group_name, data in groups.items():
        if not data["indices"]:
            print(f"{group_name}: 空组")
            continue
        
        group_min = np.min(data["lengths"])
        group_max = np.max(data["lengths"])
        group_avg = np.mean(data["lengths"])
        print(f"{group_name}:")
        print(f"  曲线数量: {len(data['indices'])}")
        print(f"  长度范围: {group_min:.6f} - {group_max:.6f}")
        print(f"  平均长度: {group_avg:.6f}")
    
    # 为每组创建新物体（使用网格）
    created_objects = []
    for group_name, data in groups.items():
        indices = data["indices"]
        if not indices:
            print(f"\n跳过空组: {group_name}")
            continue
        
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
            for i in range(orig_curve.points_length):
                point = orig_curve.points[i]
                vertices.append(point.position)
            
            # 添加边（连接曲线上的点）
            for i in range(orig_curve.points_length - 1):
                edges.append((vertex_index + i, vertex_index + i + 1))
            
            # 更新顶点索引
            vertex_index += orig_curve.points_length
        
        # 创建网格
        mesh_data.from_pydata(vertices, edges, [])
        mesh_data.update()
        
        # 创建新物体并添加到场景
        new_obj = bpy.data.objects.new(f"{obj.name}_{group_name}", mesh_data)
        new_obj.matrix_world = obj.matrix_world
        bpy.context.scene.collection.objects.link(new_obj)
        created_objects.append(new_obj)
        
        print(f"\n创建 {group_name} 组物体:")
        print(f"  包含曲线: {len(indices)} 条")
        print(f"  顶点数量: {len(vertices)} 个")
    
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
