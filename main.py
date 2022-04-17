from scene import Scene
import taichi as ti
from taichi.math import *

scene = Scene(exposure=10)
scene.set_floor(-0.9, (0.4, 0.5, 0.4))
scene.set_directional_light((-1, 1, -0.6), 0.2, (0.2, 0.2, 0.2))
GRID_SZ = 64


@ti.func
def draw_sphere(center, rad):
    region_min = ti.math.vec3(ti.max(-GRID_SZ, center[0] - rad),
                              ti.max(-GRID_SZ, center[1] - rad),
                              ti.max(-GRID_SZ, center[2] - rad))
    region_max = ti.math.vec3(ti.min(GRID_SZ, center[0] + rad),
                              ti.min(GRID_SZ, center[1] + rad),
                              ti.min(GRID_SZ, center[2] + rad))
    for x, y, z in ti.ndrange((region_min[0], region_max[0]),
                              (region_min[1], region_max[1]),
                              (region_min[2], region_max[2])):
        if (ti.Vector([x, y, z]) - center).norm_sqr() < rad * rad:
            scene.set_voxel(vec3(x, y, z), 1, vec3(0.26, 0.2, 0.2))


@ti.func
def draw_cone(begin_h, cone_h, cx, cz, rad, rfactor, mat, col):
    for y in range(begin_h, begin_h + cone_h):
        rad = int(
            (((cone_h + begin_h - y) / cone_h) * rfactor + 1 - rfactor) * rad)
        for x, z in ti.ndrange((-rad, rad), (-rad, rad)):
            if x * x + z * z < rad * rad:
                scene.set_voxel(vec3(x + cx, y, z + cz), mat, col)


@ti.func
def draw_rocket(begin_h, end_h, cone_h, cx, cz, rad, draw_flag=False):
    mat, col = 1, vec3(1.0, 1.0, 1.0)
    for y in range(begin_h, end_h):
        for x, z in ti.ndrange((-rad, rad), (-rad, rad)):
            if x * x + z * z < rad * rad:
                vx_col = col
                if draw_flag and 39 < y < 44 and -3 < x < 3 and z > 0:
                    vx_col = vec3(1.0, 0.0, 0.0)
                scene.set_voxel(vec3(x + cx, y, z + cz), mat, vx_col)
    draw_cone(end_h, cone_h, cx, cz, rad, 0.65, mat, col)


@ti.kernel
def initialize_voxels():
    # smoke
    draw_sphere(vec3(2, -69, -16), 25)
    draw_sphere(vec3(5, -68, 15), 21)
    draw_sphere(vec3(-18, -73, 0), 30)
    draw_sphere(vec3(17, -61, 2), 12)
    # fire
    FIRE_Y_MAX = -10
    draw_cone(-GRID_SZ, (FIRE_Y_MAX + GRID_SZ), 0, 0, 6, 0.7, 2,
              vec3(0.8, 0.6, 0.2))
    BODY_RAD, SIDE_RAD = 6, 4
    # body
    draw_rocket(FIRE_Y_MAX, 45, 10, 0, 0, BODY_RAD, True)
    draw_rocket(55, 60, 0, 0, 0, 1)  # tip
    # thrusters
    THRUSTER_DIST = BODY_RAD + SIDE_RAD - 1
    draw_rocket(FIRE_Y_MAX, 5, 6, -THRUSTER_DIST, 0, SIDE_RAD)
    draw_rocket(FIRE_Y_MAX, 5, 6, THRUSTER_DIST, 0, SIDE_RAD)
    draw_rocket(FIRE_Y_MAX, 5, 6, 0, THRUSTER_DIST, SIDE_RAD)
    draw_rocket(FIRE_Y_MAX, 5, 6, 0, THRUSTER_DIST, SIDE_RAD)


initialize_voxels()

scene.finish()
