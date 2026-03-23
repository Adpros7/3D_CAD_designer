# simple blue cube

import bpy
from pathlib import Path

# Deselect all currently selected objects
for obj in bpy.context.selected_objects:
    obj.select_set(False)

# Add a cube at the origin
bpy.ops.mesh.primitive_cube_add(
    size=1.0,
    calc_uvs=True,
    enter_editmode=False,
    align='WORLD',
    location=(0.0, 0.0, 0.0),
    scale=(1.0, 1.0, 1.0),
)
cube = bpy.context.active_object

# Create or reuse a simple blue material
mat_name = "SimpleBlueMaterial"
mat = bpy.data.materials.get(mat_name)
if mat is None:
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    nodes = mat.node_tree.nodes

    principled = None
    for node in nodes:
        if node.type == 'BSDF_PRINCIPLED':
            principled = node
            break
    if principled is None:
        principled = nodes.new(type='ShaderNodeBsdfPrincipled')

    # Set the base color to blue (RGBA)
    principled.inputs["Base Color"].default_value = (0.0, 0.2, 1.0, 1.0)

# Assign the material to the cube
if cube.data.materials:
    cube.data.materials[0] = mat
else:
    cube.data.materials.append(mat)

# Ensure only the cube is selected for export
for obj in bpy.context.selected_objects:
    obj.select_set(False)
cube.select_set(True)
bpy.context.view_layer.objects.active = cube

# Resolve the user's Downloads folder in a cross-platform way
downloads_path = Path.home() / "Downloads"
downloads_path.mkdir(parents=True, exist_ok=True)

stl_filepath = downloads_path / "simple_blue_cube.stl"

# Export as STL using the non-legacy exporter (Blender 4.1+)
bpy.ops.wm.stl_export(
    filepath=str(stl_filepath),
    export_selected_objects=True,
    global_scale=1.0,
    use_scene_unit=False,
    apply_modifiers=True,
)