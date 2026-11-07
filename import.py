import bpy
import sys
import subprocess

argv = sys.argv
argv = argv[argv.index("--") + 1:]
for filepath in argv[:2]:
    if bpy.app.version >= (4, 0, 0):
        bpy.ops.wm.obj_import(filepath=filepath, forward_axis='X', up_axis='Z')
    else:
        bpy.ops.import_scene.obj(filepath=filepath, axis_forward='X', axis_up='Z')

for name, color in (
    ('lanes', (0.10224, 0.10224, 0.10224, 1)),
    ('roadmarkings', (0.8, 0.3834, 0.0038, 1)),
):
    obj = bpy.data.objects[name]
    material = obj.active_material
    if material is None:
        material = bpy.data.materials.new(name=name)
        if obj.data.materials:
            obj.active_material = material
        else:
            obj.data.materials.append(material)
    material.diffuse_color = color
    # Match the shader color used for rendering and FBX export.
    material.use_nodes = True
    for node in material.node_tree.nodes:
        if node.type == 'BSDF_PRINCIPLED':
            node.inputs['Base Color'].default_value = color

bpy.data.objects['roadmarkings'].location[2] = 0.1
bpy.data.objects['roadmarkings'].rotation_euler[2] = 0.0

bpy.data.objects['roadmarkings'].parent = bpy.data.objects['lanes']
bpy.data.objects.remove(bpy.data.objects['Cube'])
bpy.data.objects.remove(bpy.data.objects['Light'])
bpy.data.objects.remove(bpy.data.objects['Camera'])
bpy.ops.export_scene.fbx(filepath=argv[2], axis_forward='X', axis_up='Z', embed_textures=True)
