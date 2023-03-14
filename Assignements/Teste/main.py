#!/usr/bin/python3
import copy

import cv2
import numpy as np
from collections import namedtuple

def main():
    image_filename = '/home/miguel/Desktop/PSR/Aula5/Ex2.1/Imagens/coiso2.png'
    image = cv2.imread(image_filename , cv2.IMREAD_COLOR) # Load an image
    screen = np.ones(image.shape) * 255

##-DICTIONARY WITH COLORS------------------------------


    dict={  'red'    : {'min': [0,0,205], 'max': [55,55,256]},
            'green'  : {'min': [0,205,0], 'max': [55,256,55]},
            'blue'   : {'min': [205,0,0], 'max': [256,55,55]},
            'yellow' : {'min': [0,200,200], 'max': [55,256,256]},
            'orange': {'min': [0, 100, 205], 'max': [55, 150, 256]},
            'violet': {'min': [0, 125, 205], 'max': [55, 175, 256]},
            'black': {'min': [0, 0, 0], 'max': [20, 20, 20]},
            'white': {'min': [240, 240, 240], 'max': [256, 256, 256]}}

    colors=['red','green','blue','yellow','orange','violet','black','white']
    n=0



    for x in colors:
        n +=1
        print(x)
        mins = np.array([dict[x]['min']])
        maxs = np.array([dict[x]['max']])
        Mask = cv2.inRange(image, mins, maxs)


##-FIND CENTROID----------------------------- (serve para depois marcar o numero de cada area como no exemplo do stor)


        try:
            cnts, _ = cv2.findContours(Mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            cnt = max(cnts, key=cv2.contourArea)
            Mask_unique = np.zeros(Mask.shape, np.uint8)
            cv2.drawContours(Mask_unique, [cnt], -1, 255, cv2.FILLED)
            Mask_unique = cv2.bitwise_and(Mask, Mask_unique)
        except:
            Mask_unique = Mask

        # Morphologicall Transformation - Closing
        kernel = np.ones((5, 5), np.uint8)
        # Mask_closed = cv2.morphologyEx(Mask_unique, cv2.MORPH_CLOSE, kernel)
        Mask_closed = cv2.dilate(Mask_unique, kernel, iterations=20)
        Mask_closed = cv2.erode(Mask_closed, kernel, iterations=20)

        # Find centroid
        try:
            M = cv2.moments(Mask_closed)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        except:
            cX = 0
            cY = 0
        centroid = (cX, cY)

        print('Centroid = [' + str(cX) + ', ' + str(cY) + ']')

        #image=cv2.putText(image,n,centroid,cv2.FONT_HERSHEY_SIMPLEX,5,(0, 0, 255),5)

# FIND CONTORNS--------------------------- (serve para fazer uma imagem a preto e branco que posteriormente vai ser pintada

        image_grey = cv2.GaussianBlur(image, (5, 5), 0)
        hsv = cv2.cvtColor(image_grey, cv2.COLOR_BGR2HSV)
        contours, hierarchy = cv2.findContours(Mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        for contour in contours:
            image_contorns=cv2.drawContours(screen, contour, -1, (0, 0, 0), 3)






        cv2.imshow('imagem',image)
        cv2.imshow('mask face', Mask)
        #cv2.imshow('imagem com contornos',image_contorns)
        cv2.imshow('imagem a pintar',screen)
        cv2.waitKey(4000)




if __name__ == '__main__':
    main()
