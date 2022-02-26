import unittest   # The test framework
import numpy as np
import datetime

from sphere import sphere
from plane import plane
from triangle import triangle
from screen import screen

from point import point
from utility import norm, normalize, reflected

from texture import texture

class Test_Shape(unittest.TestCase):

    # functional tests
    def test_sphere_intersect(self):

        # arrange
        s1 = sphere(np.array([0, 0, 0]),0.1,None)

        ro = np.array([0, 0, -1])
        rd = np.array([0, 0, 1])

        # act
        distance = s1.intersect(ro,rd)

        # assert - check distance and calculated intersection are correct
        self.assertEqual(round(distance,2), 0.9)

    # non-functional tests
    def test_sphere_intersect_performance(self):

        # arrange - add obects to the scene
        s1 = sphere(np.array([-0.3, 0, 0]),0.1,None)
        
        camera = np.array([0, 0, 1])
        scr = screen(300,200)
        points = [point(x, y) for x in range(scr.width) for y in range(scr.height)]

        # act - start timer
        startTime = datetime.datetime.now()

        for p in points:

            p.pixel = np.array([scr.xcoords[p.x], scr.ycoords[p.y], 0])

            # set the origin to the camera
            p.origin = camera
            p.direction = normalize(p.pixel - p.origin)

            i = s1.intersect(p.origin,p.direction)

        elapsed_time = datetime.datetime.now() - startTime

        # assert - check elapsed time less than target
        self.assertLessEqual(elapsed_time.total_seconds(),2)


    def test_plane_intersect(self):
        
        # arrange
        p1 = plane(np.array([-0.3, 0, 0]), np.array([-0.3, 0, 0]),texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5))
        ro = np.array([0, 0, 1])
        rd = np.array([-0.3, 0, 0])

        # act         
        distance,intersection = p1.intersect(ro,rd)

        # assert - check distance and calculated intersection are correct
        self.assertEqual(distance,0.3)
        self.assertEqual(intersection.all(),np.array([-0.3, 0, 1.0]).all())

    def test_triangle_intersect(self):

        # arrange
        p0 = np.array([-1.0,-1.0,0.0])
        p1 = np.array([1.0,-1.0,0.0])
        p2 = np.array([0.0,1.0,0.0])

        t1 = triangle(p0,p1,p2,None)
        
        ro = np.array([0, 0, -2])
        rd = np.array([0, 0, 1])

        # act
        distance  = t1.intersect(ro,rd)
        
        # assert - check distance and calculated intersection are correct
        self.assertEqual(distance,2.0)
    

if __name__ == '__main__':
    unittest.main()