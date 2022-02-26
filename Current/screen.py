import numpy as np

class screen:

    def __init__(self, width, height) -> None:
        
        self.width = width
        self.height = height

        self.ratio = float(self.width) / self.height

        self.left = -1
        self.top = 1 / self.ratio
        self.right = 1
        self.bottom = -1 / self.ratio
        
        self.xcoords = np.linspace(self.left, self.right, self.width)
        self.ycoords = np.linspace(self.top, self.bottom, self.height)
        #self.screen = (-1, 1 / self.ratio, 1, -1 / self.ratio) # left, top, right, bottom 
