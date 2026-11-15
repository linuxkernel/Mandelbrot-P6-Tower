import bpy

def apply_golden_material(target_name="PlateauMeshP6"):
    mat_name = "MandelbrotGold"
    mat = bpy.data.materials.get(mat_name)
    if not mat:
        mat = bpy.data.materials.new(name=mat_name)
    mat.use_nodes = True

    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    node_out = nodes.new(type='ShaderNodeOutputMaterial')
    node_out.location = (600, 0)

    node_bsdf = nodes.new(type='ShaderNodeBsdfPrincipled')
    node_bsdf.location = (250, 0)
    node_bsdf.inputs['Metallic'].default_value = 0.96
    node_bsdf.inputs['Roughness'].default_value = 0.18

    node_coord = nodes.new(type='ShaderNodeTexCoord')
    node_coord.location = (-700, 0)

    node_sep = nodes.new(type='ShaderNodeSeparateXYZ')
    node_sep.location = (-500, 0)

    node_ramp = nodes.new(type='ShaderNodeValToRGB')
    node_ramp.location = (-200, 100)
    # Cliff color (deep crimson-bronze) to plateau top (bright 24k gold)
    node_ramp.color_ramp.elements[0].position = 0.15
    node_ramp.color_ramp.elements[0].color = (0.45, 0.06, 0.12, 1.0)
    elem_mid = node_ramp.color_ramp.elements.new(0.65)
    elem_mid.color = (0.85, 0.55, 0.12, 1.0)
    node_ramp.color_ramp.elements[-1].position = 0.92
    node_ramp.color_ramp.elements[-1].color = (1.0, 0.84, 0.35, 1.0)

    node_noise = nodes.new(type='ShaderNodeTexNoise')
    node_noise.location = (-450, -200)
    node_noise.inputs['Scale'].default_value = 18.0
    node_noise.inputs['Detail'].default_value = 6.0

    node_bump = nodes.new(type='ShaderNodeBump')
    node_bump.location = (0, -200)
    node_bump.inputs['Strength'].default_value = 0.08

    links.new(node_coord.outputs['Object'], node_sep.inputs['Vector'])
    links.new(node_sep.outputs['Z'], node_ramp.inputs['Fac'])
    links.new(node_ramp.outputs['Color'], node_bsdf.inputs['Base Color'])

    links.new(node_coord.outputs['Object'], node_noise.inputs['Vector'])
    links.new(node_noise.outputs['Fac'], node_bump.inputs['Height'])
    links.new(node_bump.outputs['Normal'], node_bsdf.inputs['Normal'])

    links.new(node_bsdf.outputs['BSDF'], node_out.inputs['Surface'])

    obj = bpy.data.objects.get(target_name)
    if obj:
        obj.data.materials.clear()
        obj.data.materials.append(mat)
        print(f"Applied {mat_name} to {target_name}.")
    else:
        print(f"Created {mat_name}; target object '{target_name}' not found.")

if __name__ == "__main__":
    apply_golden_material()
