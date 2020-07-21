import bpy
import os
scene = context.scene
for frame in range(scene.frame_start, scene.frame_end):
    scene.frame_set(frame)
    bpy.context.view_layer.update()
    the_file = scene.name + "_" + str(scene.frame_current) + '.obj'
    bpy.ops.export_scene.obj(filepath=os.path.join(self.objs_path, the_file), check_existing=True, axis_forward='-Z', axis_up='Y', filter_glob="*.obj;*.mtl", use_selection=True, use_animation=False, use_mesh_modifiers=True, use_edges=True, use_smooth_groups=False, use_smooth_groups_bitflags=False, use_normals=False, use_uvs=False, use_materials=False, use_triangles=False, use_nurbs=False, use_vertex_groups=False, use_blen_objects=True, group_by_object=False, group_by_material=False, keep_vertex_order=True, global_scale=self.scale, path_mode='AUTO')