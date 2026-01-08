# requirements: simple grey square

import bpy
from pathlib import Path

# Create a simple square (plane) at the origin
bpy.ops.mesh.primitive_plane_add(
    size=1.0,
    enter_editmode=False,
    align='WORLD',
    location=(0.0, 0.0, 0.0),
)

plane = bpy.context.active_object

# Create or get a simple grey material and assign it to the plane
mat_name = "SimpleGreyMaterial"
mat = bpy.data.materials.get(mat_name)
if mat is None:
    mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes.get("Principled BSDF")
    if bsdf is not None:
        # Medium grey RGBA
        bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)

if plane.data.materials:
    plane.data.materials[0] = mat
else:
    plane.data.materials.append(mat)

# Ensure only the plane is selected for export
bpy.ops.object.select_all(action='DESELECT')
plane.select_set(True)
bpy.context.view_layer.objects.active = plane

# Determine the Downloads folder path (cross-platform) and STL file path
downloads_dir = Path.home() / "Downloads"
downloads_dir.mkdir(parents=True, exist_ok=True)
stl_filepath = downloads_dir / "simple_grey_square.stl"

# Export the selected plane as STL into the Downloads folder.
# Uses the non-deprecated STL export operator bpy.ops.wm.stl_export with filepath
# and export_selected_objects parameters as documented. 
bpy.ops.wm.stl_export(
    filepath=str(stl_filepath),
    export_selected_objects=True,
)