# -*- coding: utf-8 -*-

import argparse
import math
from operator import attrgetter, itemgetter

import cv2
import numpy as np

#from matplotlib import pyplot as plt
from processa_imagem import ProcessaImagem
from palo import Palo
from utils import Utils

imgName = '10'
img = cv2.imread('source-img/' + imgName + '.JPG')

utl = Utils()
pro = ProcessaImagem()
img = pro.rotacionar(img)

HEIGHT = 2300
l, img = pro.resize(img, height=HEIGHT)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
imgTmp = gray.copy()
imgTmp[:, :] = 0

img2 = gray.copy()
img2 = img2[0:200, :400]

LINHASM = 10
COLUNASM = 10

MIN_AREA = 45
MAX_AREA = 4900

quebraCol = imgTmp.shape[1] / COLUNASM
quebraRows = imgTmp.shape[0] / LINHASM
quebraCol = np.int(quebraCol)
quebraRows = np.int(quebraRows)

conta = 0
contatotalPalos = 0
contacol = 0

flat_object = img.copy()
# resize the image
ratio, flat_object_resized = pro.resize(flat_object, height=HEIGHT)
# make a copy
flat_object_resized_copy = flat_object_resized.copy()

our_cnt = None
our_cnt = pro.processaImagemRoiWarp(flat_object_resized_copy)
warped = None

CORTE = 30
HT_CORTE = 100
HB_CORTE = 150



if our_cnt is not None:
    warped = pro.for_point_warp(our_cnt / ratio, flat_object)
    ratio, warped = pro.resize(warped, height=HEIGHT)

    #utl.mostraImg("flat_object_resized_copy: ", flat_object_resized_copy)
    #cv2.imwrite("tmp/warp.png", warped)



if warped is not None:
    #gray = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
    perspect = warped
    perspect = perspect[HT_CORTE:len(perspect) - HB_CORTE, CORTE:perspect.shape[1] - CORTE]
    clone = warped[HT_CORTE:len(warped)- HB_CORTE , CORTE:warped.shape[1] - CORTE].copy()
else:
    perspect = cv2.cvtColor(flat_object_resized, cv2.COLOR_BGR2GRAY)
    perspect = perspect[HT_CORTE:len(perspect)-HB_CORTE, CORTE:perspect.shape[1] - CORTE]
    clone = flat_object_resized[HT_CORTE:len(perspect), CORTE:perspect.shape[1] - CORTE].copy()

# erosion = pro.processaImagem2(gray)
'''
for linha in range(0,quebraRows*LINHASM,quebraRows):
    conta = 0
    for coluna in range(0,quebraCol*COLUNASM,quebraCol):
        imgTmp2 = gray[linha:linha+quebraRows:,conta:quebraCol+coluna]
        #imgTmp2  = utl.brihoecontraste(imgTmp2,10,10)
        fgbg = cv2.createBackgroundSubtractorMOG2()
        fgmask = fgbg.apply(imgTmp2)
        differenceImage =  cv2.absdiff(fgmask, imgTmp2)
        erosion = pro.processaImagem3(differenceImage)
        #utl.mostraImg("erosion: ", erosion)
        imgTmp[linha:linha+quebraRows:,conta:quebraCol+coluna]=erosion
        #utl.mostraImg("imgTmp: ", imgTmp)
        #print([linha,linha+quebraRows, conta,quebraCol+coluna])
        conta = quebraCol+coluna
    #utl.mostraImg("imgTmp1: ", imgTmp)
'''
'''
img8 Intervalos {1: 177, 2:160,3:182,4:183,5:190}
'''
# gray = pro.processaImagemRoiWarpRefine(gray)


impProcessed = pro.processaImagem2(perspect)
cv2.imwrite("tmp/img-processed.png", impProcessed)

h, cnts, hx = cv2.findContours(impProcessed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

print(len(cnts))
cnts2 = cnts.copy()

# sort the contours from left-to-right and initialize the bounding box
# point colors
(cnts, boundingBoxes) = pro.sort_contours(cnts, method="top-to-bottom")

font = cv2.FONT_HERSHEY_SIMPLEX
areas = []
larguras = []
palos = []
cntsTmp = []
cnts_c = np.array(cnts)

i = 0
'''
while i < len(cnts_c):
    c = cv2.boundingRect(cnts_c[i])
    x, y, w, h = c
    area = cv2.contourArea(cnts_c[i])
    larguras.append(w)
    areas.append(area)
    if x < 50 or area < MIN_AREA or area > MAX_AREA or x > imgTmp.shape[1] - 50:
        cnts_c = np.delete(cnts_c, i)
        i = i - 1
        continue

    i = i + 1
# fim while
'''

mediaAreas = np.mean(areas)
desvioAreas = np.std(areas)
mediaLarguras = np.mean(larguras)
desvioLarguras = np.std(larguras)
print(mediaAreas)
cnts_b = cnts_c.copy()
boxes = []
i = 0
print("Total palos",len(cnts_b))
while i < len(cnts_b):
    contornos = cnts_c[i]
    x, y, w, h = cv2.boundingRect(contornos)
    area = cv2.contourArea(contornos)
    epsilion = 0.001 * cv2.arcLength(contornos, True)
    approx = cv2.approxPolyDP(contornos, epsilion, True)
    areaApprox = cv2.contourArea(approx)
    if not (x < CORTE or area < MIN_AREA or area > MAX_AREA or x > imgTmp.shape[1] - CORTE):
        rect = Palo(x, y, w, h)
        rect.setContornos(contornos)
        rect.setArea(area)
        rect.setAreApprox(areaApprox)
        rect.setApprox(approx)
        rect.soma()
        boxes.append(rect)
    i = i + 1
# fim while

listaOrdenada = []

ordem = False
div = 2
X_PALO = 10
H_PALO = 10

print('boxes antes: '+str(len(boxes)))

boxes = pro.sortByPositionXY(boxes, clone)

totalPalos = 0
conta = 0
tempo = 1
tempos = {}
i = 0
print('boxes: '+str(len(boxes)))
while i < len(boxes):
    palo = boxes[i]
    if palo.x < CORTE:
        print('nao')
    if palo.x > CORTE:

        # area = cv2.contourArea(cnts_b[i])
        if palo.area > MIN_AREA and palo.area < MAX_AREA:

            if palo.w > (2 * palo.h):

                #if conta > 40:
                tempos[tempo] = conta
                cv2.putText(clone, str(conta), (palo.x, palo.y - 2), font, 0.8, (0, 0, 255), 2)
                #cv2.rectangle(clone, (palo.x, palo.y), (palo.x + palo.w, palo.y + palo.h), (0, 255, 0), 2)
                #utl.mostraImg("cnts: ", clone)
                #if conta > 40:
                tempo = tempo + 1
                conta = 0

            elif i != len(boxes) - 1 :
                #if palo.w > mediaLarguras + desvioLarguras + 4 and palo.w < palo.h:
                    #conta = conta + 1
                    #cv2.putText(clone, str(conta), (palo.x, palo.y), font, 0.8, (0, 0, 255), 1)
                #else:

                    conta = conta + 1
                    cv2.putText(clone, str(conta), (palo.x, palo.y + palo.h + 20), font, 0.4, (0, 0, 0), 1)

            cv2.rectangle(clone, (palo.x, palo.y), (palo.x + palo.w, palo.y + palo.h), (0, 255, 0), 2)


            cv2.drawContours(clone, [palo.getApprox()], -1, (255, 0, 0), 1)
            #imgCrop = utl.recortar(imgTmp, palo)
            # _, imgCrop=pro.resize(imgCrop, height=30)
            '''
            try:
                cv2.imwrite("tmp/treinamento/" + str(i) + ".png", imgCrop)
            except ValueError:
                print(i)
                print(ValueError)
            #utl.mostraImg("cnts: ", clone)
            # print(conta)
            '''
        if i == len(boxes) - 1:
            # if conta > 40:
            print('parar')
            tempos[tempo] = conta
            break
    i = i + 1


# fim while
print("shape", imgTmp.shape)

print(tempos)
diffPalos = {}
for i in range(1, len(tempos)):
    diffPalos[i] = abs(tempos[i] - tempos[i + 1])
totalPalos = sum([int(x) for x in tempos.values()])

print(diffPalos)
print(totalPalos)
somaDiffPalos = sum([int(x) for x in diffPalos.values()])
print(somaDiffPalos)
NOR = round(somaDiffPalos * 100 / totalPalos, 1)
print("NOR: "+str(NOR))

cv2.putText(clone, "PALOS: " + str((totalPalos)), (40, 30), font, 0.9, (255, 0, 0), 2)
cv2.putText(clone, "NOR: " + str((NOR)), (220, 30), font, 0.9, (255, 0, 0), 2)
cv2.putText(clone, "INTERVALOS: " + str((tempos)), (400, 30), font, 0.9, (255, 0, 0), 2)
cv2.putText(clone, "IMAGEM: " + str((imgName)), (1200, 30), font, 0.9, (255, 0, 0), 2)
# utl.mostraImg("cnts: ", clone)
# utl.mostraImg("imgTmp: ", imgTmp)
cv2.imwrite("tmp/clone" + imgName + ".png", clone)

