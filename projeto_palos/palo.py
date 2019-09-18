import numpy as np

class Palo:

    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.area =0
        self.numero =0
        self.somaXY=0
        self.menorDistancia = 0
        self.id = 0

    def __str__(self):
        return "id:"+str(self.id)+" x:"+str(self.x)+" y: "+str(self.y)+\
               " w: "+str(self.w)+" h: "+str(self.h)+" dist:"+str(self.menorDistancia)+" area:"+str(self.area)
    def setId(self,id):
        self.id=id
    def getId(self):
        return self.id
    def setMenorDistancia(self,dist):
        self.menorDistancia=dist
    def getMenorDistancia(self):
        return self.menorDistancia
    def setContornos(self,contornos):
        self.contornos = contornos
    def getContornos(self):
        return self.contornos
    def setArea(self,area):
        self.area = area
    def getArea(self):
        return self.area
    def setNum(self,num):
        self.numero= num
    def setAreApprox(self,areaApprox):
        self.areaApprox = areaApprox
    def getAreApprox(self):
        return self.areaApprox
    def setApprox(self,approx):
        self.approx =approx
    def getApprox(self):
        return self.approx
    def soma(self):
        self.somaXY = self.x+self.y

    
        
