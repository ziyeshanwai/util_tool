import bpy
import math
from mathutils import Euler

if bpy.context.mode != 'POSE':
    bpy.ops.object.mode_set(mode='POSE')

# 获取选中的姿势骨骼
selected_pose_bones = [bone for bone in bpy.context.selected_pose_bones]

for bone in selected_pose_bones:
    # 获取骨骼的全局变换矩阵
    global_matrix = bone.matrix
    
    # 如果有父骨骼，计算局部矩阵
    if bone.parent:
        parent_inverse_matrix = bone.parent.matrix.inverted()
        local_matrix = parent_inverse_matrix @ global_matrix
    else:
        # 如果没有父骨骼，则局部矩阵等于全局矩阵
        local_matrix = global_matrix
    
    # 将全局变换矩阵转换为欧拉角
    global_euler = global_matrix.to_euler()
    
    # 将局部变换矩阵转换为欧拉角
    local_euler = local_matrix.to_euler()
    
    # 将欧拉角转换为度数
    global_euler_degrees = [math.degrees(angle) for angle in global_euler]
    local_euler_degrees = [math.degrees(angle) for angle in local_euler]
    
    # 打印结果
    print(f"Bone: {bone.name}")
    print(f"Global Euler Angles (degrees): X={global_euler_degrees[0]:.2f}, Y={global_euler_degrees[1]:.2f}, Z={global_euler_degrees[2]:.2f}")
    print(f"Local Euler Angles (degrees): X={local_euler_degrees[0]:.2f}, Y={local_euler_degrees[1]:.2f}, Z={local_euler_degrees[2]:.2f}")
