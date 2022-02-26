import numpy as np
import numba as nb
import texture
from utility import norm

class plane:
    
    def __init__(self, point, normal, texture):

        self.point = point
        self.normal = normal
        self.texture = texture

    def display(self):
        
        print(self.point)
        print(self.normal)    
        
        self.texture.display()

    def intersect(self, ray_origin, ray_direction):

        epsilon=1e-6
        ndotu = self.normal.dot(ray_direction) 

        if abs(ndotu) < epsilon:
            print ("no intersection or line is within plane")

        w = ray_origin - self.point
        si = -self.normal.dot(w) / ndotu
        Psi = w + si * ray_direction + self.point

        squared_dist = np.sum((ray_origin-Psi)**2, axis=0)
        dist = np.sqrt(squared_dist)

        return dist,Psi