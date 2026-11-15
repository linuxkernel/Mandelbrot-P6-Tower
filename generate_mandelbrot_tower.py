import bpy
import bmesh
import math

def generate_mandelbrot_tower(
    resolution=640,
    span=6.6,
    max_iter=64,
    power=6,
    height_scale=2.8,
    base_thickness=0.2
):
    mesh_name = "PlateauMeshP6"
    if mesh_name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[mesh_name], do_unlink=True)
    if mesh_name in bpy.data.meshes:
        bpy.data.meshes.remove(bpy.data.meshes[mesh_name], do_unlink=True)

    mesh = bpy.data.meshes.new(mesh_name)
    obj = bpy.data.objects.new(mesh_name, mesh)
    bpy.context.collection.objects.link(obj)
    bpy.context.view_layer.objects.active = obj

    bm = bmesh.new()
    half_span = span / 2.0
    step = span / (resolution - 1)

    verts_grid = [[None for _ in range(resolution)] for _ in range(resolution)]

    for iy in range(resolution):
        y = -half_span + iy * step
        for ix in range(resolution):
            x = -half_span + ix * step
            c = complex(x / 2.2, y / 2.2)
            z = 0j
            iters = 0
            while abs(z) <= 2.0 and iters < max_iter:
                z = (z ** power) + c
                iters += 1

            if iters == max_iter:
                z_height = height_scale
            else:
                smooth_val = iters + 1 - math.log(math.log(max(abs(z), 1.0001))) / math.log(power)
                norm_h = max(0.0, min(1.0, smooth_val / max_iter))
                z_height = base_thickness + (norm_h ** 1.6) * (height_scale - base_thickness)

            verts_grid[iy][ix] = bm.verts.new((x, y, z_height))

    bm.verts.ensure_lookup_table()

    for iy in range(resolution - 1):
        for ix in range(resolution - 1):
            v1 = verts_grid[iy][ix]
            v2 = verts_grid[iy][ix + 1]
            v3 = verts_grid[iy + 1][ix + 1]
            v4 = verts_grid[iy + 1][ix]
            bm.faces.new((v1, v2, v3, v4))

    bm.normal_update()
    bm.to_mesh(mesh)
    bm.free()

    for poly in mesh.polygons:
        poly.use_smooth = True

    print(f"Generated {mesh_name} ({resolution}x{resolution} grid, span={span}).")

if __name__ == "__main__":
    generate_mandelbrot_tower()
