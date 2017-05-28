import numpy as np

from Point import Point
from Triangle import Triangle


class TerminalEdgeAlgorithm:
    # Funcion que recibe la trinagulacion, donde
    # la triangulacion es un arreglo de triangulos.
    def __init__(self, triangulation, minAngle, canvas):
        self.triangulation = triangulation
        self.minAngle = minAngle
        self.canvas = canvas
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
        edge = terminals[0].maxEdge

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
        point = Point((edge.v1.x + edge.v2.y) / 2, (edge.v1.y + edge.v2.y) / 2)
        #triangle1 = Triangle(v1, v0, v3)
        #triangle1.t1 = triangle1.t1

        if np.cross([point.x - v1.x, point.y - v1.y], [v2.x - point.x, v2.y - point.y]) == 0:
            triangle1 = Triangle(v3, v1, point, triangle.t3, None, triangle.t2)
            triangle2 = Triangle(v2, v3, point, triangle1, triangle.t3, triangle.t1)
            triangle1.t2 = triangle2
            self.canvas.drawLine(v3, point)

        elif np.cross([point.x - v2.x, point.y - v2.y], [point.x - v3.x, point.y - v3.y]) != 0:
            triangle1 = Triangle(v1, v2, point, triangle.t1, None, triangle.t3)
            triangle2 = Triangle(v3, v1, point, triangle1, triangle.t3, triangle.t2)
            triangle1.t2 = triangle2
            self.canvas.drawLine(v1, point)

        elif np.cross([point.x - v3.x, point.y - v3.y], [point.x - v1.x, point.y - v1.y]) != 0:
            triangle1 = Triangle(v1, v2, point, None, triangle.t2, triangle.t3)
            triangle2 = Triangle(v2, v3, point, triangle.t2, triangle1, triangle.t1)
            triangle1.t1 = triangle2
            self.canvas.drawLine(v1, point)

        else:
            print "Error en funcion isBoundary!"

        #triangle2 = Triangle(v0, v2, v3)
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
        myTriangle1  = Triangle(vertex1,edge.v1,vertex2,triangle2.getTriangleWithvertex(edge.v2),None,triangle1.getTriangleWithvertex(edge.v2))
        myTriangle2 = Triangle(vertex2,edge.v2,vertex1,triangle1.getTriangleWithvertex(edge.v1),myTriangle1,triangle2.getTriangleWithvertex(edge.v1))
        myTriangle1.t2 = myTriangle1
        # Refrescar vecinos
        if myTriangle1.t2 is not None:
            myTriangle1.t1.refreshPointer(triangle2, myTriangle1)
        if myTriangle1.t3 is not None:
            myTriangle1.t3.refreshPointer(triangle1, myTriangle1)
        if myTriangle2.t1 is not None:
            triangle2.t1.refreshPointer(triangle1, myTriangle2)
        if myTriangle2.t3 is not None:
            myTriangle2.t3.refreshPointer(triangle2, myTriangle2)  # t por other
        self.triangulation.append(myTriangle1)
        self.triangulation.append(myTriangle2)
        self.canvas.deleteLine(edge.v1,edge.v2)
        self.canvas.drawLine(vertex1,vertex2)

        return [myTriangle1,myTriangle2]

    def bisection(self,triangle1,triangle2,edge):
        self.triangulation.remove(triangle1)
        self.triangulation.remove(triangle2)
        vertex1 = triangle2.getVertex(triangle1)
        vertex2 = triangle1.getVertex(triangle2)
        p=Point((edge.v1.x+edge.v2.x)/2,(edge.v1.y+edge.v2.y)/2)
        myTriangle1 = Triangle(vertex1, edge.v1, p,None,None,triangle1.getTriangleWithvertex(edge.v2))
        myTriangle2 = Triangle(edge.v1, vertex2, p,None,myTriangle1,triangle2.getTriangleWithvertex(edge.v2))
        myTriangle3 = Triangle(vertex2,edge.v2,p,None,myTriangle2,triangle2.getTriangleWithvertex(edge.v1))
        myTriangle4 = Triangle(edge.v2,vertex1,p,myTriangle1,myTriangle3,triangle1.getTriangleWithvertex(edge.v1))
        myTriangle1.t1 = myTriangle2
        myTriangle1.t2 = myTriangle4
        myTriangle2.t1 = myTriangle3
        myTriangle3.t1 = myTriangle4
        if myTriangle1.t3 is not None:
            myTriangle1.t3.refreshPointer(triangle1,myTriangle1)
        if myTriangle2.t3 is not None:
            myTriangle2.t3.refreshPointer(triangle2,myTriangle2)
        if myTriangle3.t3 is not None:
            myTriangle3.t3.refreshPointer(triangle2,myTriangle3)
        if myTriangle4.t3 is not None:
            myTriangle4.t3.refreshPointer(triangle1,myTriangle4)

        self.triangulation.append(myTriangle1)
        self.triangulation.append(myTriangle2)
        self.triangulation.append(myTriangle3)
        self.triangulation.append(myTriangle4)
        self.canvas.drawLine(vertex1,p)
        self.canvas.drawLine(p,vertex2)

        return [myTriangle1,myTriangle2,myTriangle3,myTriangle4]

    def updateBadTriangles(self, terminals):
        for triangle in terminals:
            if triangle.isBadTriangle(self.minAngle):
                self.badTriangles.append(triangle)




