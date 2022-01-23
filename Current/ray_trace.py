#imports
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sphere import sphere
from texture import texture
from light import light
from utility import norm, normalize, reflected

startTime = datetime.datetime.now()



def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [obj.intersect(ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance


class tracer:

    def __init__(self):
        
        self.width = 300
        self.height = 200

        self.max_depth = 3

        self.camera = np.array([0, 0, 1])
        self.ratio = float(self.width) / self.height
        self.screen = (-1, 1 / self.ratio, 1, -1 / self.ratio) # left, top, right, bottom 
                
        self.source = light(np.array([5, 5, 5]), texture(np.array([1, 1, 1]), np.array([1, 1, 1]), np.array([1, 1, 1]), 0, 0))
        
        
        self.objects = []
        self.path = 'Current\image.png'


    def render(self):
        
        self.image = np.zeros((self.height, self.width, 3))
        for i, y in enumerate(np.linspace(self.screen[1], self.screen[3], self.height)):
            for j, x in enumerate(np.linspace(self.screen[0], self.screen[2], self.width)):
                # screen is on origin
                origin = self.camera
                pixel = np.array([x, y, 0])
                direction = normalize(pixel - origin)

                color = np.zeros((3))
                reflection = 1

                for _ in range(self.max_depth):
                    # check for intersections
                    nearest_object, min_distance = nearest_intersected_object(self.objects, origin, direction)
                    if nearest_object is None:
                        break

                    intersection = origin + min_distance * direction
                    normal_to_surface = nearest_object.shapenormal(intersection)
                    shifted_point = intersection + 1e-5 * normal_to_surface
                    intersection_to_light = normalize(self.source.position - shifted_point)

                    nearest_distance, min_distance = nearest_intersected_object(self.objects, shifted_point, intersection_to_light)
                    intersection_to_light_distance = norm(self.source.position - intersection)
                    is_shadowed = min_distance < intersection_to_light_distance

                    if is_shadowed:
                        break

                    illumination = np.zeros((3))

                    # ambiant
                    illumination += nearest_object.texture.ambient * self.source.texture.ambient

                    # diffuse
                    illumination += nearest_object.texture.diffuse * self.source.texture.diffuse * np.dot(intersection_to_light, normal_to_surface)

                    # specular
                    intersection_to_camera = normalize(origin - intersection)
                    H = normalize(intersection_to_light + intersection_to_camera)
                    illumination += nearest_object.texture.specular * self.source.texture.specular * np.dot(normal_to_surface, H) ** (nearest_object.texture.shininess / 4)

                    # reflection
                    color += reflection * illumination
                    reflection *= nearest_object.texture.reflection

                    origin = shifted_point
                    direction = reflected(direction, normal_to_surface)

                self.image[i, j] = np.clip(color, 0, 1)
            print("%d/%d" % (i + 1, self.height))
        endTime = datetime.datetime.now()
        print(endTime - startTime)

        plt.imsave(self.path, self.image)
