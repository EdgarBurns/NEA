#imports
import numpy as np
import matplotlib.pyplot as plt
import datetime
from sphere import norm, sphere
from texture import texture
from light import light


startTime = datetime.datetime.now()

def normalize(vector):
    return vector / norm(vector)

def reflected(vector, axis):
    return vector - 2 * np.dot(vector, axis) * axis

def nearest_intersected_object(objects, ray_origin, ray_direction):
    distances = [obj.intersect(ray_origin, ray_direction) for obj in objects]
    nearest_object = None
    min_distance = np.inf
    for index, distance in enumerate(distances):
        if distance and distance < min_distance:
            min_distance = distance
            nearest_object = objects[index]
    return nearest_object, min_distance
### class
width = 300
height = 200

max_depth = 3

camera = np.array([0, 0, 1])
ratio = float(width) / height
screen = (-1, 1 / ratio, 1, -1 / ratio) # left, top, right, bottom
### class 

source = light(np.array([5, 5, 5]), texture(np.array([1, 1, 1]), np.array([1, 1, 1]), np.array([1, 1, 1]), 0, 0))

objects = [
    sphere( np.array([0.1, -0.3, 0]), 0.1, texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) ),
    sphere( np.array([-0.2, 0, -1]), 0.7, texture(np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100, 0.5 )),
    sphere( np.array([-0.3, 0, 0]), 0.15, texture(np.array([0, 0.1, 0]), np.array([0, 0.6, 0]), np.array([1, 1, 1]), 100, 0.5 )),
    sphere( np.array([0, -9000, 0]), 9000 - 0.7, texture(np.array([0.1, 0.1, 0.1]), np.array([0.6, 0.6, 0.6]), np.array([1, 1, 1]), 100, 0.5 ))
    
]


image = np.zeros((height, width, 3))
for i, y in enumerate(np.linspace(screen[1], screen[3], height)):
    for j, x in enumerate(np.linspace(screen[0], screen[2], width)):
        # screen is on origin
        pixel = np.array([x, y, 0])
        origin = camera
        direction = normalize(pixel - origin)

        color = np.zeros((3))
        reflection = 1

        for _ in range(max_depth):
            # check for intersections
            nearest_object, min_distance = nearest_intersected_object(objects, origin, direction)
            if nearest_object is None:
                break

            intersection = origin + min_distance * direction
            normal_to_surface = normalize(intersection - nearest_object.centre)
            shifted_point = intersection + 1e-5 * normal_to_surface
            intersection_to_light = normalize(source.position - shifted_point)

            nearest_distance, min_distance = nearest_intersected_object(objects, shifted_point, intersection_to_light)
            intersection_to_light_distance = norm(source.position - intersection)
            is_shadowed = min_distance < intersection_to_light_distance

            if is_shadowed:
                break

            illumination = np.zeros((3))

            # ambiant
            illumination += nearest_object.texture.ambient * source.texture.ambient

            # diffuse
            illumination += nearest_object.texture.diffuse * source.texture.diffuse * np.dot(intersection_to_light, normal_to_surface)

            # specular
            intersection_to_camera = normalize(camera - intersection)
            H = normalize(intersection_to_light + intersection_to_camera)
            illumination += nearest_object.texture.specular * source.texture.specular * np.dot(normal_to_surface, H) ** (nearest_object.texture.shininess / 4)

            # reflection
            color += reflection * illumination
            reflection *= nearest_object.texture.reflection

            origin = shifted_point
            direction = reflected(direction, normal_to_surface)

        image[i, j] = np.clip(color, 0, 1)
    print("%d/%d" % (i + 1, height))
endTime = datetime.datetime.now()
print(endTime - startTime)

plt.imsave('image.png', image)