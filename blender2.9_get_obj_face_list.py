import bpy

ob = bpy.data.objects["head_geo"].data

selected_vertex_list = [v.index for v in ob.vertices if v.select]


selected_poly_gon_vertex_list = [v.index for v in ob.polygons if v.select]  # get the selected face index

selected_face_vertec_index = [v for p in selected_poly_gon_vertex_list for v in ob.polygons[p].vertices] # get face vertex index

## get face list
face_list = []
for i in range(0, len(ob.polygons)):
    face = [v for v in ob.polygons[i].vertices]  # +1 with same with obj file blender start index from 0 not 1
    face_list.append(face)

bpy.data.objects["head_geo"].matrix_world.inverted() @ ob.vertices[0].co
bpy.data.objects["wraped_basemesh"].matrix_world @ ob.vertices[0].co