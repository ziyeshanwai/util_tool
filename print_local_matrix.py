import bpy
import math
from mathutils import Matrix

def calculate_transform_via_matrix():
    obj = bpy.context.active_object

    # 基本检查
    if not obj or obj.mode != 'POSE':
        print("错误: 请先选择骨架并进入姿态模式 (Pose Mode)。")
        return

    selected_bones = bpy.context.selected_pose_bones
    if not selected_bones:
        print("未选中任何骨骼。")
        return

    print("=" * 60)
    print(f"骨架: {obj.name} (基于矩阵逆运算解算)")
    print("=" * 60)

    for bone in selected_bones:
        # 1. 获取子骨骼在对象空间(Object Space)下的矩阵
        mat_child = bone.matrix.copy()

        # 2. 获取父骨骼矩阵并进行逆运算
        if bone.parent:
            mat_parent = bone.parent.matrix.copy()
            # 核心公式: Local = Parent_Inverse * Child
            mat_relative = mat_parent.inverted() @ mat_child
            parent_name = bone.parent.name
        else:
            # 如果没有父骨骼，它的相对矩阵就是它相对于骨架原点的矩阵
            mat_relative = mat_child
            parent_name = "None (World/Root)"

        # 3. 从计算出的相对矩阵中分解出位移、旋转和缩放
        # to_translation() 提取位移向量
        # to_euler() 提取旋转并转为欧拉角
        # to_scale() 提取缩放向量 [新增]
        loc = mat_relative.to_translation()
        rot_euler = mat_relative.to_euler('XYZ')
        scale = mat_relative.to_scale()  # <--- 获取相对缩放

        # 4. 转换为度数
        rd_x = math.degrees(rot_euler.x)
        rd_y = math.degrees(rot_euler.y)
        rd_z = math.degrees(rot_euler.z)

        print(f"骨骼: {bone.name} (父级: {parent_name})")
        print(f"  [矩阵解算] 相对位置: X={loc.x:.4f}, Y={loc.y:.4f}, Z={loc.z:.4f}")
        print(f"  [矩阵解算] 相对旋转: X={rd_x:.4f}°, Y={rd_y:.4f}°, Z={rd_z:.4f}°")
        # [新增] 打印相对缩放
        print(f"  [矩阵解算] 相对缩放: X={scale.x:.4f}, Y={scale.y:.4f}, Z={scale.z:.4f}")
        print("-" * 40)

if __name__ == "__main__":
    calculate_transform_via_matrix()