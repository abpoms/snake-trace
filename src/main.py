from Tkinter import Canvas, PhotoImage, Tk, mainloop
from scene_objects import Light, Camera, Ray, Sphere, Plane
import numpy as np
import matrix
import math
import sys


HEIGHT = 400
WIDTH = 400

world_objects = set()
light_objects = set()


def compute_camera_ray(width, height, camera, view_width, x, y):
    normalized_x = ((1.0 * x / width) - 0.5) * view_width
    normalized_y = (0.5 - (1.0 * y / height)) * view_width
    ray_direction = matrix.normalize(normalized_x * camera.right +
                                     normalized_y * camera.up +
                                     camera.direction)
    ray = Ray(origin=camera.position, vector=ray_direction)
    return ray


def compute_light(light, intersection, normal):
    to_light = matrix.normalize(light.position - intersection)
    shade = np.dot(to_light, normal)
    return max(shade, 0)


def point_on_line(ray, distance):
    return ray.origin + distance * ray.vector


def trace_ray(world, lights, ray):
    depth = float('inf')
    color = np.array([0, 0, 0])
    for obj in world:
        distance, normal = obj.get_intersection(ray)
        if distance is not None and distance < depth:
            depth = distance
            point = point_on_line(ray, distance)
            for light in lights:
                shade = compute_light(light, point, normal)
                color = obj.diffuse * (shade * 0.8 + 0.2)
    return color


def init_world(world):
    red = Sphere(center=np.array([0.0, 4.0, 6.0]),
                 radius=4.0,
                 diffuse=np.array([255, 0, 0]))
    world_objects.add(red)

    blue = Sphere(center=np.array([-5.0, 3.0, 0.0]),
                  radius=3.0)
    world_objects.add(blue)

    green = Sphere(center=np.array([5.0, 2.0, 0.0]),
                   radius=2.0,
                   diffuse=np.array([0, 255, 0]))
    world_objects.add(green)

    plane = Plane(normal=np.array([0, 1, 0]), distance=0.0)
    world_objects.add(plane)


def init_light(lights):
    light = Light(position=np.array([5.0, 5.0, -3.0]))
    lights.add(light)


def main():
    master = Tk()
    w = Canvas(master, width=WIDTH, height=HEIGHT)
    w.pack()

    img = PhotoImage(width=WIDTH, height=HEIGHT, master=master)
    w.create_image((WIDTH/2, HEIGHT/2), image=img, state="normal")

    cam = Camera()
    cam.look_at(np.array([0, 10, -8]),
                np.array([0, 0, 3.0]),
                np.array([0, 1.0, 0]))

    init_world(world_objects)
    init_light(light_objects)
    # Generate rays for each pixel and determine color
    progress_interval = HEIGHT*WIDTH / 10
    progress_tick = 0
    print 'Progress (10 ticks): [ -',
    sys.stdout.flush()
    for y in xrange(HEIGHT):
        for x in xrange(WIDTH):
            progress_tick += 1
            if progress_tick > progress_interval:
                progress_tick = 0
                print ' -',
                sys.stdout.flush()
            ray = compute_camera_ray(WIDTH, HEIGHT, cam, 3, x, y)
            color = trace_ray(world_objects, light_objects, ray)
            # TKinter requires a hex string as color input for photo image
            img.put('#%02X%02X%02X' % tuple(color), (x, y))
    print ' - ]'
    mainloop()

if __name__ == "__main__":
    main()

    