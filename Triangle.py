import sys

import math

from Edge import Edge
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
        self.maxEdge = None

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
        self.maxEdge =Edge(self.v1,self.v2)
        dist = self.v1.dist(self.v2)
        aux = self.v2.dist(self.v3)
        if (dist < aux):
            dist = aux
            self.maxEdge = Edge(self.v2, self.v3)
            triangle=self.t1
        aux = self.v3.dist(self.v1)
        if (dist < aux):
            self.maxEdge = Edge(self.v1, self.v2)
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


    def isBadTriangle(self,minAngle):
        edge1 = Edge(self.v1,self.v2)
        edge2 = Edge(self.v2,self.v3)
        edge3 = Edge(self.v3,self.v1)

        if self.ang(edge1, edge2) <= minAngle:
            return True
        elif self.ang(edge2,edge3) <= minAngle:
            return True
        elif self.ang(edge3,edge1) <= minAngle:
            return True
        return False


    def dot(self,vector1,vector2):
        return vector1[0] * vector2[0] + vector1[1] * vector2[1]


    def ang(self,edge1,edge2):
        vector1 = [(edge1.v1.x-edge1.v2.x),(edge1.v1.y - edge1.v2.x)]
        vector2 = [(edge2.v1.x-edge2.v2.x),(edge2.v1.y - edge2.v2.x)]
        dot_prod = self.dot(vector1,vector2)
        magnitude1 = self.dot(vector1,vector1)**0.5
        magnitude2 = self.dot(vector2,vector2)**0.5
        cosen = dot_prod/magnitude1/magnitude2
        angle = math.acos(cosen)
        ang_deg = math.degrees(angle)%360

        if ang_deg > 180:
            return 360 -ang_deg
        else:
            return ang_deg

    def getTriangleWithvertex(self,vertex):
        if vertex is self.v1:
            return self.t1
        elif vertex is self.v2:
            return self.t2
        elif vertex is self.v3:
            return self.t3
        print "Ocurrio un error al determinar el vecino de %s",vertex
