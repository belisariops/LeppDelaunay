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

