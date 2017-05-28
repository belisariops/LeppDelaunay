from numpy.ma import dot, empty_like

from Point import Point


class Edge:
    def __init__(self,v1,v2):
        self.v1 =v1
        self.v2 =v2

    def getMidPoint(self):
        return Point((self.v1.x+self.v2.x)/2,(self.v1.y+self.v2.y)/2)
