import numpy as np
from timeit import default_timer as timer 

total = 0

objects = [
 #   { 'center': np.array([0.1, -0.3, 0]), 'radius': 0.1, 'ambient': np.array([0.1, 0, 0.1]), 'diffuse': np.array([0.7, 0, 0.7]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
  #  { 'center': np.array([-0.2, 0, -1]), 'radius': 0.7, 'ambient': np.array([0.1, 0, 0]), 'diffuse': np.array([0.7, 0, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
  #  { 'center': np.array([-0.3, 0, 0]), 'radius': 0.15, 'ambient': np.array([0, 0.1, 0]), 'diffuse': np.array([0, 0.6, 0]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 },
    { 'center': np.array([0, -9000, 0]), 'radius': 9000 - 0.7, 'ambient': np.array([0.1, 0.1, 0.1]), 'diffuse': np.array([0.6, 0.6, 0.6]), 'specular': np.array([1, 1, 1]), 'shininess': 100, 'reflection': 0.5 }
]

def sphere_intersect(center, radius, ray_origin, ray_direction):
    b = 2 * np.dot(ray_direction, ray_origin - center)
    c = np.linalg.norm(ray_origin - center) ** 2 - radius ** 2
    delta = b ** 2 - 4 * c
    if delta > 0:
        sqrtDelta = np.sqrt(delta)
        t1 = (-b + sqrtDelta) / 2
        t2 = (-b - sqrtDelta) / 2
        if t1 > 0 and t2 > 0:
            return min(t1, t2)
    return None


for _ in (range(100)):
    ray_origin = np.array([0.1,-0.3,0])
    ray_direction = np.array([0.1,-0.3,0])
    start = timer()    
    sphere_intersect(objects[0]['center'], objects[0]['radius'], ray_origin, ray_direction)
    end = timer()
    print(end-start)
    total += end-start 
print("total =", total/100)       