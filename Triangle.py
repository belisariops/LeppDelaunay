import sys

import math

from Point import Point


class Triangle:
    def __init__(self, v1, v2, v3, t1, t2, t3):
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.bandera = False
        self.neighbour = None

    def __str__(self):
        return "Este es el triangulo [(%s,%s),(%s,%s),(%s,%s)]" % (
        self.v1.getX(), self.v1.getY(), self.v2.getX(), self.v2.getY(), self.v3.getX(), self.v3.getY())

    def getVertex(self, t):
        vertex = None
        if self.v1 != t.v1 and self.v1 != t.v2 and self.v1 != t.v3:
            vertex = self.v1
        elif self.v2 != t.v1 and self.v2 != t.v2 and self.v2 != t.v3:
            vertex = self.v2
        else:
            vertex = self.v3
        return vertex

    def refreshPointer(self, oldTriangle, newTriangle):
        if self.t1 is None and self.t2 is None and self.t3 is None:
            return

        if self.t1 is oldTriangle:
            self.t1 = newTriangle
        elif self.t2 is oldTriangle:
            self.t2 = newTriangle
        elif self.t3 is oldTriangle:
            self.t3 = newTriangle



    def getTriangleWithPoints(self,p,q):
        if (self.v1 == p and self.v2 == q) or (self.v1 == q and self.v2 == p):
            return self.t3
        elif (self.v2 == p and self.v3 == q) or (self.v2 == q and self.v3 == p):
            return self.t1
        elif (self.v1 == p and self.v3 == q) or (self.v1 == q and self.v3 == p):
            return self.t2
        return None

    def defineNeighbour(self):
        triangle = self.t3
        dist = self.v1.dist(self.v2)
        aux = self.v2.dist(self.v3)
        if (dist < aux):
            dist = aux
            self.t1
        aux = self.v3.dist(self.v1)
        if (dist < aux):
            triangle = self.t2
        return triangle

    def getTerminalTriangles(self):
        self.neighbour = self.defineNeighbour()
        if (self.neighbour is None):
            return [self,self.neighbour]
        elif (self is self.neighbour.neighbour):
            return [self,self.neighbour]
        else:
            return self.neighbour.getTerminalTriangles()

    def dotproduct(self,v1, v2):
        return sum((a * b) for a, b in zip(v1, v2))

    def length(self,v):
        return math.sqrt(self,dotproduct(v, v))

    def angle(self,v1, v2):
        return math.acos(self.dotproduct(v1, v2) / (self.length(v1) * self.length(v2)))

    def isBadTriangle(self,minAngle):
        return False


