import numpy as np
import numba as nb
import texture

class triangle:
    
    def __init__(self, v0, v1, v2, texture):

        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.texture = texture

        self.u = self.v1 - self.v0
        self.v = self.v2 - self.v0

        self.normal = np.cross(self.u, self.v)

        # compute edges
        self.edge1 = self.v1 - self.v0
        self.edge2 = self.v2 - self.v0


    def display(self):
        
        print(self.v0)
        print(self.v1)
        print(self.v2)
        
        self.texture.display()

    def shapenormal(self, intersection):
        return self.normal


    def intersect(self,ray_start, ray_vec):

        """Moeller–Trumbore intersection algorithm.

        Source
        ------

        https://docs.pyvista.org/examples/99-advanced/ray-trace-moeller.html

        Visualize the Moeller–Trumbore Algorithm — PyVista 0.33.0 documentation
        
        Parameters
        ----------
        ray_start : np.ndarray
            Length three numpy array representing start of point.

        ray_vec : np.ndarray
            Direction of the ray.

        Returns
        -------
            distance ``t``

        """

        eps = 0.000001
       
        pvec = np.cross(ray_vec, self.edge2)
        det = self.edge1.dot(pvec)

        if abs(det) < eps:  # no intersection
            return None

        inv_det = 1. / det
        tvec = ray_start - self.v0
        u = tvec.dot(pvec) * inv_det

        if u < 0. or u > 1.:  # if not intersection
            return None

        qvec = np.cross(tvec, self.edge1)
        v = ray_vec.dot(qvec) * inv_det
        if v < 0. or u + v > 1.:  # if not intersection
            return None

        t = self.edge2.dot(qvec) * inv_det
        if t < eps:
            return None

        return t

  