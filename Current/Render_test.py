import unittest   # The test framework
import numpy as np
import time

from sphere import sphere
from plane import plane
from triangle import triangle
import ray_trace
import datetime

from texture import texture

class Test_Render(unittest.TestCase):

    def test_image_building(self):

        # arrange
        spheres = [
             sphere( np.array([0.1, -0.3, 0]), 0.1, texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) ),
             sphere( np.array([-0.2, 0, -1]), 0.7, texture(np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100, 0.5 )),
             sphere( np.array([-0.3, 0, 0]), 0.15, texture(np.array([0, 0.1, 0]), np.array([0, 0.6, 0]), np.array([1, 1, 1]), 100, 0.5 )),
             sphere( np.array([0, -9000, 0]), 9000 - 0.7, texture(np.array([0.1, 0.1, 0.1]), np.array([0.6, 0.6, 0.6]), np.array([1, 1, 1]), 100, 0.5 ))  
        ]

        expectedElapsed = [3,4,6,10] 
        actualElapsed = [0,0,0,0]

        t1 = ray_trace.tracer()

        # act - increase the number of shapes and check times
        for s in range(len(spheres)):
            
            t1.objects.append(spheres[s])

            for i in range(1):

                start_time = time.time()
                t1.render(0)
                actualElapsed[s] = round(time.time() - start_time,2)

                print("%s : %s shapes : %s seconds" %  (i, s+1, actualElapsed[s]) )
            

        # assert
        self.assertLessEqual(actualElapsed,expectedElapsed)     

    def test_single_image(self):

        # arrange
        spheres = [
             sphere( np.array([0.1, -0.3, 0]), 0.1, texture(np.array([0.1, 0, 0.1]), np.array([0.7, 0, 0.7]), np.array([1, 1, 1]), 100, 0.5) ),
             sphere( np.array([-0.2, 0, -1]), 0.7, texture(np.array([0.1, 0, 0]), np.array([0.7, 0, 0]), np.array([1, 1, 1]), 100, 0.5 )),
             sphere( np.array([-0.3, 0, 0]), 0.15, texture(np.array([0, 0.1, 0]), np.array([0, 0.6, 0]), np.array([1, 1, 1]), 100, 0.5 )),
             sphere( np.array([0, -9000, 0]), 9000 - 0.7, texture(np.array([0.1, 0.1, 0.1]), np.array([0.6, 0.6, 0.6]), np.array([1, 1, 1]), 100, 0.5 ))  
        ] 

        t1 = ray_trace.tracer()

        t1.objects.append(spheres[0])
        t1.objects.append(spheres[1])
        t1.objects.append(spheres[2])
        t1.objects.append(spheres[3])
        
        # act
        startTime = datetime.datetime.now()
        t1.render(2)
        elapsed_time = datetime.datetime.now() - startTime

        # assert - check elapsed time less than target
        self.assertLessEqual(elapsed_time.total_seconds(),10)

if __name__ == '__main__':
    unittest.main()