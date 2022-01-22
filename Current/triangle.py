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

    def shapenormal(self):
        return self.normal

    @nb.njit(fastmath=False)
    def intersect_line_triangle(self,q1,q2,p1,p2,p3):
        
        def signed_tetra_volume(a,b,c,d):
            return np.sign(np.dot(np.cross(b-a,c-a),d-a)/6.0)

        s1 = signed_tetra_volume(q1,p1,p2,p3)
        s2 = signed_tetra_volume(q2,p1,p2,p3)

        if s1 != s2:
            s3 = signed_tetra_volume(q1,q2,p1,p2)
            s4 = signed_tetra_volume(q1,q2,p2,p3)
            s5 = signed_tetra_volume(q1,q2,p3,p1)
            if s3 == s4 and s4 == s5:
                n = np.cross(p2-p1,p3-p1)
                t = np.dot(p1-q1,n) / np.dot(q2-q1,n)
                return q1 + t * (q2-q1)
        return None

    def intersect(self,ray_start, ray_vec):

        """Moeller–Trumbore intersection algorithm.

        Source
        ------

        https://docs.pyvista.org/examples/99-advanced/ray-trace-moeller.html
Visualize the Moeller–Trumbore Algorithm — PyVista 0.33.0 documentation
Visualize the Moeller–Trumbore Algorithm¶. This example demonstrates the Moeller–Trumbore intersection algorithm using pyvista. For additional details, please reference the following:
docs.pyvista.org
        
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

    

    def ray_triangle_intersection(self,ray_start, ray_vec):
        """Moeller–Trumbore intersection algorithm.

        Parameters
        ----------
        ray_start : np.ndarray
            Length three numpy array representing start of point.

        ray_vec : np.ndarray
            Direction of the ray.

        triangle : np.ndarray
            ``3 x 3`` numpy array containing the three vertices of a
            triangle.

        Returns
        -------
        bool
            ``True`` when there is an intersection.

        tuple
            Length three tuple containing the distance ``t``, and the
            intersection in unit triangle ``u``, ``v`` coordinates.  When
            there is no intersection, these values will be:
            ``[np.nan, np.nan, np.nan]``

        """
        # define a null intersection
        null_inter = np.array([np.nan, np.nan, np.nan])

        # break down triangle into the individual points
        v1, v2, v3 = triangle
        eps = 0.000001

        # compute edges
        edge1 = v2 - v1
        edge2 = v3 - v1
        pvec = np.cross(ray_vec, edge2)
        det = edge1.dot(pvec)

        if abs(det) < eps:  # no intersection
            return False, null_inter
        inv_det = 1. / det
        tvec = ray_start - v1
        u = tvec.dot(pvec) * inv_det

        if u < 0. or u > 1.:  # if not intersection
            return False, null_inter

        qvec = np.cross(tvec, edge1)
        v = ray_vec.dot(qvec) * inv_det
        if v < 0. or u + v > 1.:  # if not intersection
            return False, null_inter

        t = edge2.dot(qvec) * inv_det
        if t < eps:
            return False, null_inter

        return True, np.array([t, u, v]) 