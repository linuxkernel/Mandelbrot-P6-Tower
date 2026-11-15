import bpy
import math
import colorsys

def create_rainbow_holo_rings_ground(
    num_rings=8,          # Number of concentric rings
    start_radius=4.2,     # Inner radius surrounding the tower base
    ring_spacing=0.55,    # Distance between each ring
    base_z=0.01,          # Ground-level Z coordinate
    emission_strength=8.0 # Soft, controlled light emission
):
    # 1. Clean up old holographic ring collection/objects
    col_name = "HoloRingSystem"
    if col_name in bpy.data.collections:
        old_col = bpy.data.collections[col_name]
        for obj in list(old_col.objects):
            bpy.data.objects.remove(obj, do_unlink=True)
        bpy.data.collections.remove(old_col)

    if "HolographicRings" in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects["HolographicRings"], do_unlink=True)

    # Create a dedicated collection for clean scene organization
    ring_col = bpy.data.collections.new(col_name)
    bpy.context.scene.collection.children.link(ring_col)

    # 2. Function to generate a rainbow material for a given hue (0.0 to 1.0)
    def create_rainbow_mat(name, hue, strength):
        mat = bpy.data.materials.get(name)
        if not mat:
            mat = bpy.data.materials.new(name=name)
            mat.use_nodes = True
            nodes = mat.node_tree.nodes
            links = mat.node_tree.links
            nodes.clear()

            node_out = nodes.new(type='ShaderNodeOutputMaterial')
            node_out.location = (400, 0)

            node_mix = nodes.new(type='ShaderNodeMixShader')
            node_mix.location = (200, 0)

            node_trans = nodes.new(type='ShaderNodeBsdfTransparent')
            node_trans.location = (0, 100)

            node_emit = nodes.new(type='ShaderNodeEmission')
            node_emit.location = (0, -100)
            
            # Convert HSV hue to RGB for a gorgeous rainbow gradient
            rgb = colorsys.hsv_to_rgb(hue, 0.85, 1.0)
            node_emit.inputs['Color'].default_value = (rgb[0], rgb[1], rgb[2], 1.0)
            node_emit.inputs['Strength'].default_value = strength

            # Layer Weight for soft translucent edges
            node_lw = nodes.new(type='ShaderNodeLayerWeight')
            node_lw.location = (-250, 0)
            node_lw.inputs['Blend'].default_value = 0.35

            links.new(node_lw.outputs['Facing'], node_mix.inputs['Fac'])
            links.new(node_trans.outputs['BSDF'], node_mix.inputs[1])
            links.new(node_emit.outputs['Emission'], node_mix.inputs[2])
            links.new(node_mix.outputs['Shader'], node_out.inputs['Surface'])
        return mat

    # 3. Generate Concentric 3D Torus Rings at Ground Level
    for i in range(num_rings):
        radius = start_radius + (i * ring_spacing)
        minor_rad = 0.018  # Sleek, uniform ring thickness
        z_offset = base_z + (i * 0.002)  # Barely perceptible height step so they don't z-fight

        bpy.ops.mesh.primitive_torus_add(
            major_segments=128,
            minor_segments=16,
            major_radius=radius,
            minor_radius=minor_rad,
            location=(0.0, 0.0, z_offset)
        )
        ring_obj = bpy.context.active_object
        ring_obj.name = f"HoloRing_Rainbow_{i+1:02d}"

        # Smooth shading
        for poly in ring_obj.data.polygons:
            poly.use_smooth = True

        # Calculate evenly spaced hue along the color wheel
        hue_val = i / max(1, num_rings - 1)
        mat_rainbow = create_rainbow_mat(f"HoloMat_Hue_{i:02d}", hue_val, emission_strength)
        ring_obj.data.materials.append(mat_rainbow)

        # Move to HoloRingSystem collection
        for col in list(ring_obj.users_collection):
            col.objects.unlink(ring_obj)
        ring_col.objects.link(ring_obj)

    print(f"Successfully created {num_rings} ground-level rainbow holographic rings!")

if __name__ == "__main__":
    create_rainbow_holo_rings_ground()
