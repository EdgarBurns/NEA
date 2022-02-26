#imports
import numpy as np
import matplotlib.pyplot as plt
import datetime
from multiprocessing import Pool, current_process
from itertools import product

from sphere import sphere
from triangle import triangle
from point import point

from texture import texture
from light import light
from screen import screen
from utility import norm, normalize, reflected

startTime = datetime.datetime.now()


class tracer:

    def __init__(self):
        
        self.max_depth = 3

        self.camera = np.array([0, 0, 1])
        self.screen = screen(300,200)
        self.source = light(np.array([5, 5, 5]), texture(np.array([1, 1, 1]), np.array([1, 1, 1]), np.array([1, 1, 1]), 0, 0))
             
        self.objects = [] #[triangle(np.array([-0.2, 0, -1]),np.array([0.2, 0, -1]),np.array([0, 1, -1]),texture(np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100, 0.5 ))]

        self.path = 'Current\image.png'

    def nearest_intersected_object(self, ray_origin, ray_direction):
        distances = [obj.intersect(ray_origin, ray_direction) for obj in self.objects]
        nearest_object = None
        min_distance = np.inf
        for index, distance in enumerate(distances):
            if distance and distance < min_distance:
                min_distance = distance
                nearest_object = self.objects[index]
        return nearest_object, min_distance

    def render_image(self, p):


        # screen is on origin (z=0)
        p.pixel = np.array([self.screen.xcoords[p.x], self.screen.ycoords[p.y], 0])

        # set the origin to the camera
        p.origin = self.camera
        p.direction = normalize(p.pixel - p.origin)

        p.color = np.zeros((3))
        p.reflection = 1

        for _ in range(self.max_depth):

            # check for intersections
            p.nearest_object, p.min_distance = self.nearest_intersected_object(p.origin, p.direction)

            if p.nearest_object is None:
                break

            p.intersection = p.origin + p.min_distance * p.direction
            p.normal_to_surface = p.nearest_object.shapenormal(p.intersection)
            p.shifted_point = p.intersection + 1e-5 * p.normal_to_surface
            p.intersection_to_light = normalize(self.source.position - p.shifted_point)

            p.nearest_distance, p.min_distance = self.nearest_intersected_object(p.shifted_point, p.intersection_to_light)
            p.intersection_to_light_distance = norm(self.source.position - p.intersection)

            # check if shadowed
            if p.min_distance < p.intersection_to_light_distance:
                break

            p.illumination = np.zeros((3))

            # ambient
            p.illumination += p.nearest_object.texture.ambient * self.source.texture.ambient

            # diffuse
            p.illumination += p.nearest_object.texture.diffuse * self.source.texture.diffuse * np.dot(p.intersection_to_light, p.normal_to_surface)

            # specular
            p.intersection_to_camera = normalize(p.origin - p.intersection)
            H = normalize(p.intersection_to_light + p.intersection_to_camera)
            p.illumination += p.nearest_object.texture.specular * self.source.texture.specular * np.dot(p.normal_to_surface, H) ** (p.nearest_object.texture.shininess / 4)

            # reflection
            p.color += p.reflection * p.illumination
            p.reflection *= p.nearest_object.texture.reflection

            p.origin = p.shifted_point
            p.direction = reflected(p.direction, p.normal_to_surface)

        if p.color[0] != 0 or p.color[1] != 0 or p.color[2]:
            print("Rendering: %d %d - Colour %s %s %s" % (p.x, p.y, p.color[0],p.color[1],p.color[2]))
        self.image[p.y, p.x] = np.clip(p.color, 0, 1)

    def render(self,process_count):
        
        self.image = np.zeros((self.screen.height, self.screen.width, 3))

        points = [point(x, y) for x in range(self.screen.width) for y in range(self.screen.height)]

        startTime = datetime.datetime.now()

        if process_count == 0:
            for p in points:
                self.render_image(p)
        else:
            with Pool(processes=process_count) as pool:
                results = pool.map(self.render_image, points)

        print("Completed : Processes = %s, Elapsed = %s" % (process_count, datetime.datetime.now() - startTime))

        plt.imsave(self.path, self.image)

        print("Saved File")
