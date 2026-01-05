# green sphere

import bpy
import os

# Optional: clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Create a UV sphere
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1.0,
    enter_editmode=False,
    align='WORLD',
    location=(0.0, 0.0, 0.0),
    scale=(1.0, 1.0, 1.0),
)
sphere = bpy.context.active_object

# Create a green material using Principled BSDF
mat = bpy.data.materials.new(name="GreenMaterial")
mat.use_nodes = True
nodes = mat.node_tree.nodes
principled = nodes.get("Principled BSDF")

if principled:
    # RGBA: pure green
    principled.inputs["Base Color"].default_value = (0.0, 1.0, 0.0, 1.0)

# Assign the material to the sphere
if sphere.data.materials:
    sphere.data.materials[0] = mat
else:
    sphere.data.materials.append(mat)

# Build Downloads directory path in a cross-platform way
home_dir = os.path.expanduser("~")
downloads_dir = os.path.join(home_dir, "Downloads")

# Create Downloads directory if it doesn't exist
os.makedirs(downloads_dir, exist_ok=True)

# Full export path for the STL file
export_path = os.path.join(downloads_dir, "green_sphere.stl")

# Ensure only the sphere is selected for export
bpy.ops.object.select_all(action='DESELECT')
sphere.select_set(True)
bpy.context.view_layer.objects.active = sphere

# Export the selected sphere as STL to the Downloads folder
bpy.ops.export.stl(
    filepath=export_path,
    use_selection=True
)
