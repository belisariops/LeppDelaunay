import Tkinter
import random

import time

import Delaunay

from Point import Point


class Canvas:
    def __init__(self,w,h):
        self.delaunay = Delaunay.Delaunay(self,w,h)
        self.tk = Tkinter.Tk()
        self.tk.wm_title("Delaunay Triangulation")
        self.canvas = Tkinter.Canvas(self.tk, bg="white", height=h, width=w)
        self.w =w
        self.h =h
        self.canvas.bind("<Button-1>", self.callback)
        self.canvas.focus_set()
        self.canvas.bind('<t>',self.test)
        self.canvas.bind('<g>', self.grid)
        self.canvas.bind('<s>', self.simpleGrid)
        self.canvas.bind('<r>', self.randomPoint)
        self.canvas.bind('<d>', self.restartCanvas)
        self.canvas.pack()
        self.tk.mainloop()

    def test(self,event):

        self.callback(Point(680,self.h-445))
        self.callback(Point(960,self.h-370))
        self.callback(Point(350,self.h-345))

    def simpleGrid(self,event):
        self.callback(Point(480, self.h - 560))
        self.callback(Point(880, self.h - 560))
        self.callback(Point(480,self.h-160))
        self.callback(Point(880,self.h-160))
        self.callback(Point(480,self.h - 360))
        self.callback(Point(880, self.h - 360))
        self.callback(Point(680, self.h - 560))
        self.callback(Point(680, self.h - 360))
        self.callback(Point(680, self.h - 160))

    def randomPoint(self,event):
        self.callback(Point(random.randint(0,self.w),random.randint(0,self.h)))

    def grid(self,event):
        localX = 340
        for i in range (20):
            localY = 690
            localX +=30
            for j in range (20):
                localY -= 30
                self.callback(Point(localX,self.h -localY))
                self.canvas.update()

    def restartCanvas(self,event):
        self.canvas.delete("all")
        self.delaunay = Delaunay.Delaunay(self,self.w,self.h)


    def callback(self, event):
        #print "clicked at", event.x, event.y
        self.delaunay.click(Point(event.x,event.y))
        self.drawPoint(event.x,event.y)

    def drawPoint(self,x,y):
        self.canvas.create_oval(x-3,y-3,x+3,y+3,fill='blue')

    def drawCenter(self,x,y):
        self.canvas.create_oval(x-3,y-3,x+3,y+3,fill='black')

    #Tambien se transforma la coordenada y al sistema de coordenadas del canvas
    def drawLine (self,p,q):
        self.canvas.create_line(p.x,self.h-p.y,q.x,self.h-q.y,fill='red',width=1.3)

    def deleteLine(self,p,q):
        self.canvas.create_line(p.x,self.h-p.y,q.x,self.h-q.y,fill='yellow',width=1.3)
