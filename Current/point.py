import numpy as np

class point:
    
    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.color = np.zeros((3))
        self.reflection = 1
