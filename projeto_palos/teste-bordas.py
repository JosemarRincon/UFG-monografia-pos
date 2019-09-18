
import cv2
import numpy as np
 
# Carrega a imagem original
image = cv2.imread('9p.jpg')

# Aplica os respectivos filtros
kernel = np.ones((6,6),np.float32)/25
filter2D = cv2.filter2D(image,-1,kernel)
blur = cv2.blur(image,(5,5))
gaussianBlur = cv2.GaussianBlur(image,(15,15),0)
median = cv2.medianBlur(image,5)
bilateralFilter = cv2.bilateralFilter(image,9,75,75)

#kernel = np.ones((15,15),np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(6,6))
blackhat = cv2.morphologyEx(bilateralFilter, cv2.MORPH_RECT, kernel)
cv2.imwrite("image.png", blackhat)
#utl.mostraImg("blackhat", blackhat)
#adaptiveThreshold = cv2.adaptiveThreshold(blackhat,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,5)
#utl.mostraImg("adaptiveThreshold", adaptiveThreshold)
#blur = cv2.GaussianBlur(blackhat, (3, 3), 0)
#(ret, binarization) = cv2.threshold(blackhat, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU )
#utl.mostraImg("thresh", binarization)
kernel = np.ones((3,3),np.uint8)
dilation = cv2.dilate(blackhat,kernel,iterations = 1)
#utl.mostraImg("dilation", dilation)
erosion = cv2.erode(dilation,kernel,iterations = 1)
adaptiveThreshold = cv2.adaptiveThreshold(blackhat,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY,25,5)
cv2.imwrite("image.png", adaptiveThreshold)
# Escreve o nome de cada filtro na imagem corresponerosion
font = cv2.FONT_HERSHEY_SIMPLEX
cv2.putText(image,'Original Image',(5,320), font, cv2.LINE_AA)
cv2.putText(filter2D,'Filter 2D',(45,320), font, 1, (0,0,255), 2, cv2.LINE_AA)
cv2.putText(blur,'Blur',(80,320), font, 1, (0,0,255), 2, cv2.LINE_AA)
cv2.putText(gaussianBlur,'Gaussian Blur',(10,320), font, 1, (0,0,255), 2, cv2.LINE_AA)
cv2.putText(median,'Median',(60,320), font, 1, (0,0,255), 2, cv2.LINE_AA)
cv2.putText(bilateralFilter,'Bilateral Filter',(10,320), font, 1, (0,0,255), 2, cv2.LINE_AA)

# Concatena as imagens para gerar a imagem de saida
tempImage1 = np.concatenate((image, median, gaussianBlur), axis=1)
tempImage2 = np.concatenate((bilateralFilter, blur, filter2D), axis=1)
finalImage = np.concatenate((tempImage1, tempImage2), axis=0)

# Salva a imagem
cv2.imwrite("image.png", finalImage)
# Mostra a imagem final concatenada
#cv2.imshow("Final Image", finalImage)
# Aguarda tecla para finalizar
cv2.waitKey(0)