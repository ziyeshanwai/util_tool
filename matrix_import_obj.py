import bpy
import os
import math
from pathlib import Path

def import_and_arrange_objs(folder_path, spacing=2.0):
    """
    导入指定文件夹中的所有OBJ文件并按16:9宽高比的网格排列在X-Z平面
    :param folder_path: OBJ文件所在的文件夹路径
    :param spacing: 模型之间的间距（默认2.0）
    """
    # 清空当前场景
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    
    # 获取文件夹中的所有OBJ文件
    folder = Path(folder_path)
    obj_files = [f for f in folder.iterdir() if f.suffix.lower() == '.obj']
    num_objs = len(obj_files)
    
    if num_objs == 0:
        print("未找到OBJ文件")
        return
    
    # 计算16:9宽高比的网格布局
    target_ratio = 16/9  # 目标宽高比
    
    # 计算最佳行数和列数
    best_rows = None
    best_cols = None
    best_ratio_diff = float('inf')
    
    # 尝试不同的行数配置，找到最接近16:9的比例
    for rows in range(1, num_objs + 1):
        cols = math.ceil(num_objs / rows)
        current_ratio = cols / rows
        
        # 计算当前比例与目标比例的差异
        ratio_diff = abs(current_ratio - target_ratio)
        
        # 如果找到更接近的比例，更新最佳配置
        if ratio_diff < best_ratio_diff:
            best_ratio_diff = ratio_diff
            best_rows = rows
            best_cols = cols
    
    rows = best_rows
    columns = best_cols
    rows = 9
    columns = 30
    print(f"找到 {num_objs} 个OBJ文件")
    print(f"排列布局: {rows} 行 x {columns} 列 (比例: {columns/rows:.2f}:1 ≈ 16:9)")
    
    # 导入并排列所有OBJ文件
    for i, obj_file in enumerate(obj_files):
        # 计算网格位置
        row = i // columns
        col = i % columns
        
        # 计算位置坐标（X和Z方向）
        # 16:9布局不需要额外调整Z轴比例
        pos_x = (col - (columns - 1) / 2) * spacing
        pos_z = -((row - (rows - 1) / 2)) * spacing * 1.5  # 负号使排列从顶部开始
        
        # 导入OBJ
        bpy.ops.wm.obj_import(filepath=str(obj_file))
        
        # 获取最新导入的对象
        imported = bpy.context.selected_objects[-1]
        imported.location = (pos_x, 0, pos_z)
        
        print(f"已导入: {obj_file.name} 位置: ({pos_x:.2f}, {pos_z:.2f})")

# 使用示例
folder_path = "E:\PluginsSale\BlendShapeExporter\Samples\BSOutput\Head\Metahuman"
import_and_arrange_objs(folder_path, spacing=25)
