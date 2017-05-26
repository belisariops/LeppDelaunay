class Point:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x
    def getY(self):
        return self.y

    def __str__(self):
        return "Este es el punto (%s,%s)"%(self.x,self.y)

    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False
    def dist(self,point):
        return pow(pow(point.x - self.x,2)+pow(point.y-self.y,2),0.5)