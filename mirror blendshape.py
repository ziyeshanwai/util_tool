import bpy
import mathutils
from mathutils import Vector, kdtree
import math

def mirror_blendshape_with_soft_transition():
    # 配置参数
    MIRROR_AXIS = 'X'             # 镜像轴（X/Y/Z）
    FALLOFF_RADIUS = 0.1          # 影响半径（单位：米）
    SOURCE_KEY = "CTRL_expressions.eyeBlinkL"           # 源形态键名称
    TARGET_KEY = "CTRL_expressions.eyeBlinkR"           # 目标形态键名称
    FALLOFF_CURVE = 'LINEAR'      # 衰减曲线类型（LINEAR/SMOOTH/ROOT/SPHERE）

    obj = bpy.context.active_object
    mesh = obj.data

    # 验证形态键
    if not obj.data.shape_keys:
        raise Exception("物体没有形态键")
    
    key_blocks = obj.data.shape_keys.key_blocks
    if SOURCE_KEY not in key_blocks:
        raise Exception(f"找不到源形态键 {SOURCE_KEY}")

    # 创建/获取目标形态键
    if TARGET_KEY not in key_blocks:
        obj.shape_key_add(name=TARGET_KEY)
    
    source_key = key_blocks[SOURCE_KEY]
    target_key = key_blocks[TARGET_KEY]
    basis_key = key_blocks[0]

    # 构建顶点空间KD树（基于基础形态）
    kd = kdtree.KDTree(len(mesh.vertices))
    for i, v in enumerate(basis_key.data):
        kd.insert(v.co, i)
    kd.balance()

    # 预处理：收集所有发生位移的顶点
    deformed_verts = []
    for i in range(len(mesh.vertices)):
        delta = source_key.data[i].co - basis_key.data[i].co
        if delta.length > 0.0001:
            deformed_verts.append(i)

    # 生成影响区域映射表
    influence_map = {i: [] for i in range(len(mesh.vertices))}
    
    for src_idx in deformed_verts:
        # 计算镜像坐标
        src_co = basis_key.data[src_idx].co
        mirrored_co = Vector(src_co)
        mirrored_co.x *= -1  # 根据镜像轴调整

        # 查找镜像区域顶点
        for (co, idx, dist) in kd.find_range(mirrored_co, FALLOFF_RADIUS):
            distance = (co - mirrored_co).length
            influence_map[idx].append( (src_idx, distance) )

    # 处理每个顶点
    for vert_idx in influence_map:
        if not influence_map[vert_idx]:
            continue

        total_weight = 0.0
        blended_delta = Vector()
        basis_co = basis_key.data[vert_idx].co

        # 混合所有影响源
        for src_idx, distance in influence_map[vert_idx]:
            # 计算衰减权重
            ratio = distance / FALLOFF_RADIUS
            if ratio >= 1:
                continue

            # 选择衰减曲线
            if FALLOFF_CURVE == 'LINEAR':
                weight = 1 - ratio
            elif FALLOFF_CURVE == 'SMOOTH':
                weight = 1 - (3 * ratio**2 - 2 * ratio**3)
            elif FALLOFF_CURVE == 'ROOT':
                weight = 1 - math.sqrt(ratio)
            elif FALLOFF_CURVE == 'SPHERE':
                weight = math.sqrt(1 - ratio**2)
            
            # 获取源顶点形变向量
            src_delta = source_key.data[src_idx].co - basis_key.data[src_idx].co
            mirrored_delta = Vector(src_delta)
            mirrored_delta.x *= -1  # 镜像形变方向

            # 累加影响
            blended_delta += mirrored_delta * weight
            total_weight += weight

        if total_weight > 0:
            # 应用混合形变（保留原始形态键数据）
            final_co = basis_co + blended_delta / total_weight
            target_key.data[vert_idx].co = final_co

# 执行函数
mirror_blendshape_with_soft_transition()
