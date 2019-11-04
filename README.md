# util_tool
记录我一些关于三维模型常用的工具代码，会不断更新
- 更新日志  
- 注意blender的脚本都是在2.79版本下测试通过的，2.80 python 的API发生了变化  

bpy.data.objects['Cube'].select = True    # 2.7x  
bpy.data.objects['Cube'].select_set(True) # 2.8  
obj = bpy.context.window.scene.objects[0]
bpy.context.view_layer.objects.active = obj    # 'obj' is the active object now


-----------------------
