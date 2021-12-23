import unittest   # The test framework
from sphere import sphere
from texture import texture

class Test_Sphere(unittest.TestCase):
    def test_intersect(self):
        self.assertEqual(4,4)


if __name__ == '__main__':
    unittest.main()