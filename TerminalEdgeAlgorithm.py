import numpy as np

from Point import Point
from Triangle import Triangle


class TerminalEdgeAlgorithm:
    # Funcion que recibe la trinagulacion, donde
    # la triangulacion es un arreglo de triangulos.
    def __init__(self, triangulation, minAngle):
        self.triangulation = triangulation
        self.minAngle = minAngle
        # Arreglo de malos triangulos
        self.badTriangles = []

        # Se itera sobre la triangulacion, buscando triangulos que tengan un angulo < al angulo minimo.
        for triangle in triangulation:
            if (triangle.isBadTriangle(minAngle)):
                self.badTriangles.append(triangle)

        while len(self.badTriangles) > 0:
            self.lepp(self.badTriangles[0])

    def lepp(self, triangle):
        terminals = triangle.getTerminalTriangles()
        edge = terminals[2]

        if (terminals[1] is None):
            terminals = self.isInBoundary(terminals[0], edge)

        elif (self.isLocalyDelaunay(terminals[0], terminals[1])):
            terminals = self.flipTerminalEdge(terminals[0], terminals[1], edge)

        else:
            terminals = self.bisection(terminals[0], terminals[1], edge)

        self.updateBadTriangles(terminals)

    def isInBoundary(self, triangle, edge):
        self.triangulation.remove(triangle)
        v1 = triangle.v1
        v2 = triangle.v2
        v3 = triangle.v3
        v0 = Point((edge.v1.x + edge.v2.y) / 2, (edge.v1.y + edge.v2.y) / 2)
        triangle1 = Triangle(v1, v0, v3)
        triangle2 = Triangle(v0, v2, v3)
        self.triangulation.append(triangle1)
        self.triangulation.append(triangle2)
        return [triangle1, triangle2]

    def isLocalyDelaunay(self, triangle1, triangle2):
        vertex = triangle1.getVertex(triangle2)
        if (self.inCircle(triangle1, vertex) > 0):
            return True
        return False

    # >0 si p esta dentro del circulo circunscrito en el trianglo
    def inCircle(self, t, p):
        m = np.matrix([[t.v1.x - p.x, t.v1.y - p.y, pow((t.v1.x - p.x), 2) + pow((t.v1.y - p.y), 2)],
                       [t.v2.x - p.x, t.v2.y - p.y, pow((t.v2.x - p.x), 2) + pow((t.v2.y - p.y), 2)],
                       [t.v3.x - p.x, t.v3.y - p.y, pow((t.v3.x - p.x), 2) + pow((t.v3.y - p.y), 2)]])
        det = np.linalg.det(m)
        return det

    def flipTerminalEdge(self, triangle1, triangle2, edge):
        self.triangulation.remove(triangle1)
        self.triangulation.remove(triangle2)
        vertex1 = triangle2.getVertex(triangle1)
        vertex2 = triangle1.getVertex(triangle2)
        myTriangle1  = Triangle(vertex1,edge.v1,vertex2)
        myTriangle2 = Triangle(vertex2,edge.v2,vertex1)
        self.triangulation.append(myTriangle1)
        self.triangulation.append(myTriangle2)
        return [myTriangle1,myTriangle2]

    def bisection(self,triangle1,triangle2,edge):
        self.triangulation.remove(triangle1)
        self.triangulation.remove(triangle2)
        vertex1 = triangle2.getVertex(triangle1)
        vertex2 = triangle1.getVertex(triangle2)
        p=Point((edge.v1.x+edge.v2.x)/2,(edge.v1.y+edge.v2.y)/2)
        myTriangle1 = Triangle(vertex1, edge.v1, p)
        myTriangle2 = Triangle(edge.v1, vertex2, p)
        myTriangle3 = Triangle(vertex2,edge.v2,p)
        myTriangle4 = Triangle(edge.v2,vertex1,p)
        self.triangulation.append(myTriangle1)
        self.triangulation.append(myTriangle2)
        self.triangulation.append(myTriangle3)
        self.triangulation.append(myTriangle4)
        return [myTriangle1,myTriangle2,myTriangle3,myTriangle4]

    def updateBadTriangles(self, terminals):
        for triangle in terminals:
            if (triangle.isBadTriangle(self.minAngle)):
                self.badTriangles.append(triangle)




