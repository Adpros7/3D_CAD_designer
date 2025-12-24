# simple blue cube

import bpy
from pathlib import Path

# Create a cube at the origin
bpy.ops.mesh.primitive_cube_add()
cube = bpy.context.active_object

# Create a blue material
material = bpy.data.materials.new(name="SimpleBlueMaterial")
material.use_nodes = True

bsdf = material.node_tree.nodes.get("Principled BSDF")
if bsdf is not None:
    bsdf.inputs["Base Color"].default_value = (0.0, 0.0, 1.0, 1.0)  # RGBA, pure blue

# Assign the material to the cube
if cube.data.materials:
    cube.data.materials[0] = material
else:
    cube.data.materials.append(material)

# Prepare selection for STL export (only the cube)
bpy.ops.object.select_all(action='DESELECT')
cube.select_set(True)
bpy.context.view_layer.objects.active = cube

# Determine the path to the user's Downloads folder
downloads_dir = Path.home() / "Downloads"
downloads_dir.mkdir(parents=True, exist_ok=True)

stl_filepath = downloads_dir / "simple_blue_cube.stl"

# Export the selected cube as STL to the Downloads folder
bpy.ops.export_mesh.stl(
    filepath=str(stl_filepath),
    use_selection=True
)