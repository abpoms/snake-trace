import numpy as np
import math


def normalize(array):
    return array / np.linalg.norm(array)


def translate(v):
    return np.matrix(
        [
            [1.0, 0.0, 0.0, v[0]],
            [0.0, 1.0, 0.0, v[1]],
            [0.0, 0.0, 1.0, v[2]],
            [0.0, 0.0, 0.0, 1.0]
        ])


def perspective(fov_y, aspect, z_near, z_far):
    rad = math.radians(fov_y)
    tan_half_fov = math.tan(rad / 2)
    return np.matrix(
        [
            [1 / (aspect * tan_half_fov), 0.0, 0.0, 0.0],
            [0.0, 1 / tan_half_fov, 0.0, 0.0],
            [0.0, 0.0, (z_far + z_near) / (z_far - z_near), 1.0],
            [0.0, 0.0, (2 * z_far * z_near) / (z_far - z_near), 0.0]
        ])


def look_at(eye, center, up):
    f = normalize(eye - center)
    u = normalize(up)
    s = normalize(np.cross(f, u))
    u = np.cross(s, f)
    return np.matrix(
        [
            [s[0], u[0], f[0], 1.0],
            [s[1], u[1], f[1], 1.0],
            [s[2], u[2], f[2], 1.0],
            [-np.dot(s, eye), -np.dot(u, eye), np.dot(f, eye), 1.0]
        ])
