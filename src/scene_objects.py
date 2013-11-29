import numpy as np
import matrix
import math


class Light(object):
    def __init__(self):
        self.position = np.array([0, 0, 0])
        self.intensity = 10


class Camera(object):
    def __init__(self):
        self.position = np.array([0, 0, 0])
        self.direction = np.array([0, 0, 0])
        self.right = np.array([0, 0, 0])
        self.up = np.array([0, 0, 0])

    def look_at(self, eye, center, up):
        self.position = eye
        self.direction = matrix.normalize(center - eye)
        self.up = matrix.normalize(up)
        self.right = matrix.normalize(np.cross(self.direction, self.up))
        self.up = np.cross(self.right, self.direction)


class Ray(object):
    def __init__(self):
        self.origin = np.array([0.0, 0.0, 0.0])
        self.vector = np.array([0.0, 0.0, 0.0])

    def __str__(self):
        return "origin: " + str(self.origin) + ", vector: " + str(self.vector)


class Plane(object):
    def __init__(self):
        pass


class Sphere(object):
    def __init__(self):
        self.center = np.array([0.0, 0.0, 0.0])
        self.radius = 0
        self.diffuse = np.array([0, 0, 255.0])

    def get_intersection(self, ray):
        c = (self.center - ray.origin)
        c_distance_sqred = (c ** 2).sum()
        proj_on_ray = np.dot(c, ray.vector)
        d = (self.radius ** 2 - (c_distance_sqred - proj_on_ray ** 2))
        if (d >= 0):
            d = math.sqrt(d)
            v = proj_on_ray
            intersection_point = ray.origin + (v - d) * ray.vector
            # find normal
            normal = matrix.normalize(intersection_point - self.center)
            return intersection_point, normal
        return None, None
