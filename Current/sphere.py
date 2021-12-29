import numpy as np
import numba as nb
import texture

@nb.njit(fastmath=True)
def norm(l):
    s = 0.
    for i in range(l.shape[0]):
        s += l[i]**2
    return np.sqrt(s)

class sphere:
    
    def __init__(self, centre, radius, texture):
        self.centre = centre
        self.radius = radius
        self.texture = texture

    def display(self):
        
        print(self.centre)
        print(self.radius)    
        
        print(self.texture.ambient)  
        print(self.texture.diffuse)  
        print(self.texture.specular)  
        print(self.texture.shininess)  
        print(self.texture.reflection)  

    def intersect(self, ray_origin, ray_direction):
        b = 2 * np.dot(ray_direction, ray_origin - self.centre)
        c = norm(ray_origin - self.centre) ** 2 - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            sqrtDelta = np.sqrt(delta)
            t1 = (-b + sqrtDelta) / 2
            t2 = (-b - sqrtDelta) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None