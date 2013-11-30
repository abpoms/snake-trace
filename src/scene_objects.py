import numpy as np
import matrix
import math

np_array_zero = np.array([0.0, 0.0, 0.0])


class Light(object):
    def __init__(self,
                 position=None,
                 intensity=1):
        self.position = np.array([0.0, 0.0, 0.0]) if position is None \
            else position
        self.intensity = intensity


class Camera(object):
    def __init__(self,
                 position=None,
                 direction=None,
                 up=None):
        self.position = np.array([0, 0, 0]) if position is None else position
        self.direction = np.array([0, 0, 1]) if direction is None \
            else direction
        self.up = np.array([0, 1, 0]) if up is None else up
        self.__compute_right_up()

    def look_at(self, eye, center, up):
        self.position = eye
        self.direction = matrix.normalize(center - eye)
        self.up = matrix.normalize(up)
        self.__compute_right_up()

    def __compute_right_up(self):
        self.right = matrix.normalize(np.cross(self.direction, self.up))
        self.up = np.cross(self.right, self.direction)


class Ray(object):
    def __init__(self,
                 origin=None,
                 vector=None):
        self.origin = np.array([0, 0, 0]) if origin is None else origin
        self.vector = np.array([0, 0, 1]) if vector is None else vector

    def __str__(self):
        return "origin: %s, vector: %s".format(str(self.origin),
                                               str(self.vector))


class Plane(object):
    def __init__(self,
                 normal=None,
                 distance=5,
                 diffuse=None):
        self.normal = np.array([0, 0, -1]) if normal is None else normal
        self.distance = distance
        self.diffuse = np.array([255, 255, 255]) if diffuse is None \
            else diffuse

    def get_intersection(self, ray):
        numerator = -self.distance - np.dot(ray.origin, self.normal)
        denominator = np.dot(ray.vector, self.normal)
        if denominator != 0:
            t = numerator / denominator
            if t > 0:
                return t, self.normal
        return None, None


class Sphere(object):
    def __init__(self,
                 center=None,
                 radius=1,
                 diffuse=None):
        self.center = np.array([0.0, 0.0, 0.0]) if center is None else center
        self.radius = radius
        self.diffuse = np.array([0, 0, 255.0]) if diffuse is None else diffuse

    def get_intersection(self, ray):
        c = (self.center - ray.origin)
        c_distance_sqred = (c**2).sum()
        proj_on_ray = np.dot(c, ray.vector)
        d = self.radius ** 2 - (c_distance_sqred - proj_on_ray ** 2)
        if d >= 0:
            d = math.sqrt(d)
            v = proj_on_ray / np.linalg.norm(ray.vector)
            distance = v - d
            intersection_point = ray.origin + distance * ray.vector
            # find normal
            normal = matrix.normalize(intersection_point - self.center)
            return distance, normal
        return None, None
