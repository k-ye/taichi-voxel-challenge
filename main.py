from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.05, (1.0, 1.0, 1.0))
GRID_SZ = 64


@ti.func
def draw_sphere(center, rad):
    region_min = ti.math.vec3(ti.max(-GRID_SZ, center[0] - rad),
                              ti.max(-GRID_SZ, center[1] - rad),
                              ti.max(-GRID_SZ, center[2] - rad))
    region_max = ti.math.vec3(ti.min(GRID_SZ, center[0] + rad),
                              ti.min(GRID_SZ, center[1] + rad),
                              ti.min(GRID_SZ, center[2] + rad))
    r2 = rad * rad
    # for x in range(region_min[0], region_max[0]):
    #   scene.set_voxel(vec3(x, 0, 0), 2, vec3(1, 1, 1))
    for x, y, z in ti.ndrange((region_min[0], region_max[0]), (region_min[1], region_max[1]), (region_min[2], region_max[2])):
      dist2 = x * x + y * y + z * z
      if dist2 < r2:
        scene.set_voxel(vec3(x, y, z), 2, vec3(1, 1, 1))
    


@ti.kernel
def initialize_voxels():
    draw_sphere(vec3(0,0,0), 10)


initialize_voxels()

scene.finish()
