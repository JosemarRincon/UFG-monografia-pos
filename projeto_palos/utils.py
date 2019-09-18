import cv2
import numpy as np
from matplotlib import pyplot as plt
import math
class Utils:

    def __init__(self):
        self.METODO = 1
        
    def recortar(self,img,palo):
        img2 = img[palo.y:palo.y+palo.h , palo.x:palo.x+palo.w]
        #img.h=palo.h
        #img.w=palo.w
        #img.x=palo.x
        #img.y=palo.y
        return img2

    def brihoecontraste(self, img, contrast, brightness,metodo=2):
        #metodo 1 para numpy e metoro 2 para opencv

        if metodo == 1:
            # Convert to signed 16 bit. this will allow values less than zero and
            # greater than 255
            img = np.int16(img)  
            img = img*(contrast/127 + 1) - contrast + brightness

            # we now have an image that has been adjusted for brightness and
            # contrast, but we need to clip values not in the range 0 to 255
            img = np.clip(img, 0, 255)  # force all values to be between 0 and 255

            # finally, convert image back to unsigned 8 bit integer
            img = np.uint8(img)
        elif metodo == 2:

            #call addWeighted function, which performs:
            #    dst = src1*alpha + src2*beta + gamma
            # we use beta = 0 to effectively only operate on src1
            img = cv2.addWeighted(img, 1. + contrast/127., img, 0, brightness-contrast)
        return img

    
    def calcThreshold(self,h):
        soma=0
        conta =0
        for i  in range(0,h.size):
            if h[i] > 0:
                conta = conta+1
                soma = soma + h[i]
            if i == (h.size-1):
                mediaIntensidade = np.int(soma/conta)
                print('media: ',mediaIntensidade)
        valida=False
        trehold_in =0
        trehold_out =0
        #h = np.sort(h,axis=0,kind='heapsort')
        for i  in range(0,h.size):
            if i > 0 and h[i] > (mediaIntensidade/2):
                if not valida:
                    valida =True
                    trehold_in=i
                    print(h[i],i)
                if i < h.size-1:
                    if h[i+1] < (mediaIntensidade/2):
                        trehold_out =i
                        print(h[i],i)
        return trehold_in,trehold_out

    def ordenaRect(o,x):
       return x
        

   
  

    def mostraImg(self,titulo,img):
        cv2.imshow(titulo, img)
        key = cv2.waitKey(0)
        if key == 27 :
            print(key)
            cv2.destroyAllWindows()
    
    def rotate (self,src,angle):
       
        #(alt, lar) = img.shape[:2]
        (lar, alt) = src
        centro = (alt/2,lar/2)
        M = cv2.getRotationMatrix2D(centro,angle,1.0)
        #img_rotate = cv2.warpAffine(src,dst,M,(alt, lar))
        return M
    def mostraHistograma(self,h):
        plt.figure()
        plt.title("Histograma P&B")
        plt.xlabel("Intensidade")
        plt.ylabel("Qtde de Pixels")
        plt.plot(h)
        plt.xlim([0, 256])
        plt.show()

    def distancia(self,x1,x2,y1,y2):
        if x2 > x1:
            d = math.sqrt( ((x2-x1)**2)+ ((y2-y1)**2))
        return float(d)

