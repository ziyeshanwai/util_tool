###1.blender中选择指定顶点并打打印其索引
bpy.ops.object.mode_set(mode = 'EDIT')
##用鼠标右键选择点
bpy.ops.object.mode_set(mode = 'OBJECT')
selected_verts = [v for v in bpy.context.active_object.data.vertices if v.select]
ind = []
for sv in selected_verts:
     print(sv.index)
	 ind.append(sv)


###2.基于给定的索引选择点 与前面配合使用效果最佳
import bpy
ind = [0, 5, 7]
bpy.ops.object.mode_set(mode = 'OBJECT')
obj = bpy.context.active_object
bpy.ops.object.mode_set(mode = 'EDIT') 
bpy.ops.mesh.select_mode(type="VERT")
bpy.ops.mesh.select_all(action = 'DESELECT')
bpy.ops.object.mode_set(mode = 'OBJECT')
for i in ind:
    obj.data.vertices[i].select = True
bpy.ops.object.mode_set(mode = 'EDIT')