from Tkinter import Canvas, PhotoImage, Tk, mainloop
from scene_objects import Light, Camera, Ray, Sphere, Plane
import numpy as np
import matrix

HEIGHT = 800
WIDTH = 800

world_objects = set()
light_objects = set()


def compute_camera_ray(width, height, camera, x, y):
    normalized_x = ((1.0 * x / width) - 0.5) * 4
    normalized_y = (0.5 - (1.0 * y / height)) * 4
    ray_direction = matrix.normalize(normalized_x * camera.right +
                                     normalized_y * camera.up +
                                     camera.direction)
    ray = Ray()
    ray.origin = camera.position
    ray.vector = ray_direction
    return ray


def compute_light(light, intersection, normal):
    to_light = matrix.normalize(light.position - intersection)
    shade = np.dot(to_light, normal)
    if shade > 0:
        return shade
    return 0


def trace_ray(world, lights, ray):
    for obj in world:
        point, normal = obj.get_intersection(ray)
        if point is not None:
            for light in lights:
                shade = compute_light(light, point, normal)
                return obj.diffuse * (shade * 0.8 + 0.2)
    return np.array([0, 0, 0])


def main():
    master = Tk()
    w = Canvas(master, width=WIDTH, height=HEIGHT)
    w.pack()

    img = PhotoImage(width=WIDTH, height=HEIGHT, master=master)
    w.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

    cam = Camera()
    cam.look_at(np.array([0, 5, -10]),
                np.array([0, 0, 0]),
                np.array([0, 1.0, 0]))

    sphere = Sphere()
    sphere.radius = 4
    #world_objects.add(sphere)
    red = Sphere()
    red.center = np.array([0.0, -1.0, 0.0])
    red.radius = 4.0
    world_objects.add(red)

    plane = Plane()
    plane.normal = np.array([0, 1, 0])
    plane.distance = 4
    world_objects.add(plane)

    light = Light()
    light.position = np.array([5.0, 5.0, -3.0])
    light_objects.add(light)

    # Generate rays for each pixel and determine color
    for y in xrange(HEIGHT):
        for x in xrange(WIDTH):
            ray = compute_camera_ray(WIDTH, HEIGHT, cam, x, y)
            color = trace_ray(world_objects, light_objects, ray)
            # TKinter requires a hex string as color input for photo image
            img.put('#%02X%02X%02X' % tuple(color), (x, y))
    mainloop()

if __name__ == "__main__":
    pass
    ##main()

    