import bpy # type: ignore
from pathlib import Path

# Optional: clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create a simple UV sphere
bpy.ops.mesh.primitive_uv_sphere_add(
    radius=1.0,
    enter_editmode=False,
    align='WORLD',
    location=(0.0, 0.0, 0.0)
)
sphere = bpy.context.active_object

# Make shading smooth (optional, but usually nicer)
bpy.ops.object.shade_smooth()

# Create a gray material
mat = bpy.data.materials.new(name="SimpleGrayMaterial")
mat.use_nodes = True
bsdf = mat.node_tree.nodes.get("Principled BSDF")
if bsdf:
    # Medium gray color RGBA
    bsdf.inputs["Base Color"].default_value = (0.5, 0.5, 0.5, 1.0)

# Assign the material to the sphere
if sphere.data.materials:
    sphere.data.materials[0] = mat
else:
    sphere.data.materials.append(mat)

# Make sure only the sphere is selected for export
bpy.ops.object.select_all(action='DESELECT')
sphere.select_set(True)
bpy.context.view_layer.objects.active = sphere

# Determine the user's Downloads folder in a cross-platform way
downloads_dir = Path.home() / "Downloads"
downloads_dir.mkdir(parents=True, exist_ok=True)

# Set the output STL file path
stl_path = downloads_dir / "simple_gray_sphere.stl"

# Export the selected sphere as STL
bpy.ops.wm.stl_export(
    filepath=str(stl_path),
    export_selected_objects=True
)

print(f"STL exported to: {stl_path}")
