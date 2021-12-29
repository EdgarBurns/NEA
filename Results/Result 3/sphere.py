import numpy as np

class sphere:
    def __init__(self, centre, radius, ambient, diffuse, specular, shininess, reflection):
        self.centre = centre
        self.radius = radius
        self.ambient = ambient
        self.diffuse = diffuse
        self.specular = specular
        self.shininess = shininess
        self.reflection = reflection

    def display(self):
        print(self.centre)
        print(self.radius)    
        print(self.ambient)  
        print(self.diffuse)  
        print(self.specular)  
        print(self.shininess)  
        print(self.reflection)  

    def intersect(self, ray_origin, ray_direction):
        b = 2 * np.dot(ray_direction, ray_origin - self.centre)
        c = np.linalg.norm(ray_origin - self.centre) ** 2 - self.radius ** 2
        delta = b ** 2 - 4 * c
        if delta > 0:
            sqrtDelta = np.sqrt(delta)
            t1 = (-b + sqrtDelta) / 2
            t2 = (-b - sqrtDelta) / 2
            if t1 > 0 and t2 > 0:
                return min(t1, t2)
        return None