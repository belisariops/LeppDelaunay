import math
import numpy as np
from Point import Point
from Triangle import Triangle


class Delaunay:
    def __init__(self, canvas, width, height):
        h = math.sqrt(3) * width / 2
        x = (height + h) * 2 / math.sqrt(3)
        self.points = [Point(-x, -800), Point(width + x, -800), Point(width / 2, height + h)]
        self.triangles = [Triangle(self.points[0], self.points[1], self.points[2], None, None, None)]
        self.canvas = canvas
        self.height = height
        self.c = 0
        self.counter = 1
        self.edge = None

    def click(self, point):
        correctedAxisPoint = Point(point.x, self.height - point.y)
        self.addPoint(correctedAxisPoint)
        self.compute(correctedAxisPoint)

    def addPoint(self, point):
        self.points.append(point)

    def pointPosition(self, p0, p1, p2):
        return (p1.getX() - p0.getX()) * (p2.getY() - p0.getY()) - (p2.getX() - p0.getX()) * (p2.getY() - p0.getY())

    # 0 no, 1 si, -1 en un segmento del triangulo
    def isInTriangle(self, t, p):
        det1 = (((t.v2.x - t.v1.x) * (p.y - t.v1.y)) - ((t.v2.y - t.v1.y) * (p.x - t.v1.x)))
        det2 = (t.v3.x - t.v2.x) * (p.y - t.v2.y) - (t.v3.y - t.v2.y) * (p.x - t.v2.x)
        det3 = (t.v1.x - t.v3.x) * (p.y - t.v3.y) - (t.v1.y - t.v3.y) * (p.x - t.v3.x)
        if det1 > 0 and det2 > 0 and det3 > 0:
            return 1
        elif (det1 == 0 and det2>0 and det3>0) or (det2 == 0 and det1>0 and det3>0) or (det3 == 0 and det2>0 and det1>0):
            return -1
        else:
            return 0

    def vertexOfTriangle(self, v, triangle):
        if v == triangle.v1 or v == triangle.v2 or v == triangle.v3:
            return True
        else:
            return False

    # >0 si p esta dentro del circulo circunscrito en el trianglo
    def inCircle(self, t, p):
        m = np.matrix([[t.v1.x - p.x, t.v1.y - p.y, pow((t.v1.x - p.x), 2) + pow((t.v1.y - p.y), 2)],
                       [t.v2.x - p.x, t.v2.y - p.y, pow((t.v2.x - p.x), 2) + pow((t.v2.y - p.y), 2)],
                       [t.v3.x - p.x, t.v3.y - p.y, pow((t.v3.x - p.x), 2) + pow((t.v3.y - p.y), 2)]])
        det = np.linalg.det(m)
        return det


    def legalizeTriangle(self, t):
        vertex = None
        other = t.t3

        if other != None:
            # Obtengo el vertice que no pertenece a t
            vertex = other.getVertex(t)

            # Calculo al determinante de la matriz para ver si esta dentro del circulo
            if self.inCircle(t, vertex) > 0:
                triangle1 = Triangle(t.v1, vertex, t.v3, None, None, None)
                triangle2 = Triangle(vertex, t.v2, t.v3, t.t1, triangle1,other.getTriangleWithPoints(vertex,t.v2)) #other.t3)
                triangle1.t1 = triangle2
                triangle1.t2 = t.t2
                triangle1.t3 = other.getTriangleWithPoints(triangle1.v1, triangle1.v2)

                # Refrescar vecinos
                if triangle1.t2 is not None:
                    triangle1.t2.refreshPointer(t, triangle1)
                if triangle1.t3 is not None:
                    triangle1.t3.refreshPointer(other, triangle1)#t por other
                if triangle2.t1 is not None:
                    triangle2.t1.refreshPointer(t, triangle2)
                if triangle2.t3 is not None:
                    triangle2.t3.refreshPointer(other, triangle2)#t por other

                #Elimino el triangulo que se encontraba en el arreglo yu participo del cambio de diagonales
                try:
                    self.triangles.remove(other)
                except:
                    print "%s no existe en el arreglo " % other

                #Borro linea (la coloreo amarillo)
                self.canvas.deleteLine(triangle1.v1, triangle2.v2)

                #Reviso si los nuevos triangulos cumplen con Delaunay
                self.legalizeTriangle(triangle1)
                self.legalizeTriangle(triangle2)
                return

            #Cumple con el test del circulo, lo agrego al arreglo y lo dibujo
            else:
                self.triangles.append(t)
                self.canvas.drawLine(t.v2, t.v3)
                self.canvas.drawLine(t.v1, t.v3)
                return
        else:
            self.triangles.append(t)
            self.counter += 1
            self.canvas.drawLine(t.v2, t.v3)
            self.canvas.drawLine(t.v1, t.v3)
            return





    #Esta funcion se llama al ingresar cada punto
    def compute(self, point):
        # Por ahora se buscara el triangulo que contiene al punto de manera secuencial
        for triangle in self.triangles:
            # El punto se encuentra dentro del triangulo
            isIntriangle = self.isInTriangle(triangle, point)
            if isIntriangle != 0:
                # Guardamos el triangulo
                v1 = triangle.v1
                v2 = triangle.v2
                v3 = triangle.v3
                t1 = triangle.t1
                t2 = triangle.t2
                t3 = triangle.t3
                # Lo removemos del arreglo
                self.triangles.remove(triangle)
                # Creamos los 3 nuevos triangulos que el punto forma
                triangle1 = triangle2 = triangle3 = triangle4 = None

                #Revisamos los casos colineales
                if np.cross([point.x - v1.x, point.y - v1.y], [v2.x - point.x, v2.y - point.y]) != 0:
                    triangle1 = Triangle(v1, v2, point, None, None, triangle.getTriangleWithPoints(v1, v2))
                if np.cross([point.x - v2.x, point.y - v2.y], [point.x - v3.x, point.y - v3.y]) != 0:
                    triangle2 = Triangle(v2, v3, point, None, None, triangle.getTriangleWithPoints(v2, v3))
                if np.cross([point.x - v3.x, point.y - v3.y], [point.x - v1.x, point.y - v1.y]) != 0:
                    triangle3 = Triangle(v3, v1, point, None, None, triangle.getTriangleWithPoints(v3, v1))

                #Configuracion de cada uno de los casos colineales
                if triangle1 is None and triangle2 is not None and triangle3 is not None:
                    #Creamos los triangulos
                    vertex = t3.getVertex(triangle)
                    triangle1 = Triangle(v1, vertex, point, None, None, None)
                    triangle4 = Triangle(vertex, v2, point, None, None, None)
                    triangle1.t1 = triangle4
                    triangle1.t2 = triangle3
                    triangle1.t3 = t3.getTriangleWithPoints(v1, vertex)
                    triangle2.t1 = triangle3
                    triangle2.t2 = triangle4
                    triangle3.t1 = triangle1
                    triangle3.t2 = triangle2
                    triangle4.t1 = triangle2
                    triangle4.t2 = triangle1
                    triangle4.t3 = t3.getTriangleWithPoints(vertex, v2)
                    #Removemos el triangulo vecino
                    self.triangles.remove(t3)


                    #Actualizamos vecinos
                    if t1 is not None:
                        t1.refreshPointer(triangle, triangle2)
                    if t2 is not None:
                        t2.refreshPointer(triangle, triangle3)
                    if triangle1.t3 is not None:
                        triangle1.t3.refreshPointer(t3, triangle1)
                    if triangle4.t3 is not None:
                        triangle4.t3.refreshPointer(t3, triangle4)

                    self.legalizeTriangle(triangle1)
                    self.legalizeTriangle(triangle2)
                    self.legalizeTriangle(triangle3)
                    self.legalizeTriangle(triangle4)

                #Lo mismo nuevamente
                elif triangle1 is not None and triangle2 is None and triangle3 is not None:
                    vertex = t1.getVertex(triangle)
                    triangle2 = Triangle(v2, vertex, point, None, None, None)
                    triangle4 = Triangle(vertex, v3, point, None, None, None)
                    triangle1.t1 = triangle2
                    triangle1.t2 = triangle3
                    triangle2.t1 = triangle4
                    triangle2.t2 = triangle1
                    triangle2.t3 = t1.getTriangleWithPoints(v2, vertex)
                    triangle3.t1 = triangle1
                    triangle3.t2 = triangle4
                    triangle4.t1 = triangle3
                    triangle4.t2 = triangle2
                    triangle4.t3 = t1.getTriangleWithPoints(vertex, v3)
                    self.triangles.remove(t1)
                    if t3 is not None:
                        t3.refreshPointer(triangle, triangle1)
                    if t2 is not None:
                        t2.refreshPointer(triangle, triangle3)
                    if triangle2.t3 is not None:
                        triangle2.t3.refreshPointer(t1, triangle2)
                    if triangle4.t3 is not None:
                        triangle4.t3.refreshPointer(t1, triangle4)
                    self.legalizeTriangle(triangle1)
                    self.legalizeTriangle(triangle2)
                    self.legalizeTriangle(triangle3)
                    self.legalizeTriangle(triangle4)

                #Lo mismo
                elif triangle1 != None and triangle2 != None and triangle3 is None:
                    vertex = t2.getVertex(triangle)
                    triangle3 = Triangle(v3, vertex, point, None, None, None)
                    triangle4 = Triangle(vertex, v1, point, None, None, None)
                    triangle1.t1 = triangle2
                    triangle1.t2 = triangle4
                    triangle2.t1 = triangle3
                    triangle2.t2 = triangle1
                    triangle3.t1 = triangle4
                    triangle3.t2 = triangle2
                    triangle3.t3 = t1.getTriangleWithPoints(v3, vertex)
                    triangle4.t1 = triangle1
                    triangle4.t2 = triangle3
                    triangle4.t3 = t1.getTriangleWithPoints(vertex, v1)

                    self.triangles.remove(t2)
                    if t1 is not None:
                        t1.refreshPointer(triangle, triangle2)
                    if t3 is not None:
                        t3.refreshPointer(triangle, triangle1)
                    if triangle3.t3 is not None:
                        triangle3.t3.refreshPointer(t2, triangle3)
                    if triangle4.t3 is not None:
                        triangle4.t3.refreshPointer(t2, triangle4)

                    self.legalizeTriangle(triangle1)
                    self.legalizeTriangle(triangle2)
                    self.legalizeTriangle(triangle3)
                    self.legalizeTriangle(triangle4)

                #Caso no colineal
                else:
                    #Configuramos vecinos
                    triangle1.t1 = triangle2
                    triangle1.t2 = triangle3
                    triangle2.t1 = triangle3
                    triangle2.t2 = triangle1
                    triangle3.t1 = triangle1
                    triangle3.t2 = triangle2
                    #Actualizacion de vecinos
                    if t1 is not None:
                        t1.refreshPointer(triangle, triangle2)
                    if t2 is not None:
                        t2.refreshPointer(triangle, triangle3)
                    if t3 is not None:
                        t3.refreshPointer(triangle, triangle1)
                    #Se legalizan los triangulos creados
                    # -----------------------
                    self.legalizeTriangle(triangle1)
                    self.legalizeTriangle(triangle2)
                    self.legalizeTriangle(triangle3)
                    # -----------------------
                break

