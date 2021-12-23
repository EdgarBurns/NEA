import texture
class rectangle:
    def __init__(self, bleft, tright, texture) -> None:
        
        self.bleft   = bleft
        self.tright  = tright
        self.texture = texture

        self.width   = tright[0] - bleft[0]
        self.height  = tright[1] - bleft[1]
        self.depth   = tright[2] - bleft[2]
    
    def intersect():
        