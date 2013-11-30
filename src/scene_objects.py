import numpy as np
import matrix
import math

np_array_zero = np.array([0.0, 0.0, 0.0])


class Light(object):
    def __init__(self,
                 position=None,
                 intensity=None):
        self.position = position
        self.intensity = intensity
        if position is None:
            self.position = np_array_zero
        if intensity is None:
            self.intensity = 10


class Camera(object):
    def __init__(self,
                 position=None,
                 direction=None,
                 up=None):
        self.position = position
        self.direction = direction
        self.up = up
        if position is None:
            self.position = np.array([0, 0, 0])
        if direction is None:
            self.direction = np.array([0, 0, 1])
        if up is None:
            self.up = np.array([0, 1, 0])
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
        self.origin = origin
        self.vector = vector
        if origin is None:
            self.origin = np.array([0, 0, 0])
        if vector is None:
            self.vector = np.array([0, 0, 1])

    def __str__(self):
        return "origin: %s, vector: %s".format(str(self.origin),
                                               str(self.vector))


class Plane(object):
    def __init__(self,
                 normal=None,
                 distance=None,
                 diffuse=None):
        self.normal = normal
        self.distance = distance
        self.diffuse = diffuse
        if normal is None:
            self.normal = np.array([0, 0, -1])
        if distance is None:
            self.distance = 5
        if diffuse is None:
            self.diffuse = np.array([255, 255, 255])

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
                 radius=None,
                 diffuse=None):
        self.center = center
        self.radius = radius
        self.diffuse = diffuse
        if center is None:
            self.center = np.array([0.0, 0.0, 0.0])
        if radius is None:
            self.radius = 0
        if diffuse is None:
            self.diffuse = np.array([0, 0, 255.0])

    def get_intersection(self, ray):
        c = (self.center - ray.origin)
        c_distance_sqred = (c**2).sum()
        proj_on_ray = np.dot(c, ray.vector)
        d = self.radius ** 2 - (c_distance_sqred - proj_on_ray ** 2)
        if d >= 0:
            d = math.sqrt(d)
            v = proj_on_ray
            distance = v - d
            intersection_point = ray.origin + distance * ray.vector
            # find normal
            normal = matrix.normalize(intersection_point - self.center)
            return distance, normal
        return None, None
