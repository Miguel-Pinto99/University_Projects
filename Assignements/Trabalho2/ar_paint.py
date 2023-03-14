#!/usr/bin/env python3

import argparse
import copy
from functools import partial

import cv2
import numpy as np
from colorama import Fore, Style
import json
import math
from time import ctime

global coord_prev
global FlagMouse
global draw_geom

coord_prev = (0,0)
FlagMouse = False
draw_rect = False
draw_circ = False
draw1 = False
draw2 = False

def mouse_callback(event, x, y, flags, param, screen, color, radius, shake_prevention):

    global coord_prev
    global FlagMouse
    global draw_rect,draw_circ
    global draw1,draw2
    global centro,screen_last

    print('Coords: X = ' + str(x) + ', Y = ' + str(y))

    centroid = (x,y)
    coord = centroid

    if event == cv2.EVENT_LBUTTONDOWN and draw_circ == False and draw_rect == False:
        FlagMouse = True
        thickness = -1
        radius2 = round(radius/2)
        screen = cv2.circle(screen, coord, radius2, color, thickness)

    elif event == cv2.EVENT_MOUSEMOVE and FlagMouse == True and draw_circ == False and draw_rect == False:
        painting(screen, centroid, color, radius, shake_prevention)

    elif event == cv2.EVENT_LBUTTONUP:
        FlagMouse = False


## DESENHAR RETANGULO
    if event == cv2.EVENT_LBUTTONDOWN & draw_rect == True:
        centro = (x,y)
        screen_last=screen
        draw1 = True


    elif event == cv2.EVENT_MOUSEMOVE:
        if draw1 == True:
            cv2.rectangle(screen_last,centro,centroid,color,radius)

    elif event == cv2.EVENT_LBUTTONUP:




        draw1 = False
        draw_rect = False



# DESENHAR CIRCULO
    if event == cv2.EVENT_LBUTTONDOWN & draw_circ == True:
        centro = (x,y)
        draw2 = True
        screen_last=screen

    elif event == cv2.EVENT_MOUSEMOVE:

        if draw2 == True:

            point1 = np.array(centro)
            point2 = np.array(centroid)
            dist = int(np.linalg.norm(point1 - point2))
            print(dist)
            cv2.circle(screen_last, centro, dist, color, radius)

    elif event == cv2.EVENT_LBUTTONUP:
        draw2 = False
        draw_circ = False





def KeyFunction(screen, key, color, radius):

    global draw_rect
    global draw_circ

    if key == ord('r'):
        color = [0, 0, 255]
        print('Color RED')
    elif key == ord('g'):
        color = [0, 255, 0]
        print('Color GREEN')
    elif key == ord('b'):
        color = [255, 0, 0]
        print('Color BLUE')
    elif key == ord('y'):
        color = [0, 255, 255]
        print('Color YELLOW')
    elif key == ord('k'):
        color = 0
        print('Color BLACK')

    if key == ord('c'):
        screen[:, :, :] = 255
        print('CLEAR')

    if key == 171:  # '+'
        radius = radius + 2
        print('Bigger point')
    if key == 173:  # '-'
        radius = radius - 2
        print('Smaller point')

    if radius >= 25:
        radius = 25
    elif radius <= 4:
        radius = 4

    if key == ord('o'):
        draw_rect = True
        draw_circ = False

    if key == ord('i'):
        draw_circ = True
        draw_rect = False

    return screen, color, radius


def Masking(range_of_limits, image):

    mins = np.array([range_of_limits['limits']['B']['min'], range_of_limits['limits']['G']['min'], range_of_limits['limits']['R']['min']])
    maxs = np.array([range_of_limits['limits']['B']['max'], range_of_limits['limits']['G']['max'], range_of_limits['limits']['R']['max']])

    Mask = cv2.inRange(image, mins, maxs)

    # Find largest contour in mask
    try:
        cnts, _ = cv2.findContours(Mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnt = max(cnts, key=cv2.contourArea)
        Mask_unique = np.zeros(Mask.shape, np.uint8)
        cv2.drawContours(Mask_unique, [cnt], -1, 255, cv2.FILLED)
        Mask_unique = cv2.bitwise_and(Mask, Mask_unique)
    # If there is a black mask, there are not objects
    except:
        Mask_unique = Mask

    # Morphologicall Transformation - Closing
    kernel = np.ones((5, 5), np.uint8)
    # Mask_closed = cv2.morphologyEx(Mask_unique, cv2.MORPH_CLOSE, kernel)
    Mask_closed = cv2.dilate(Mask_unique, kernel, iterations = 20)
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

    # Find Bounding Box
    try:
        x, y, w, h = cv2.boundingRect(cnt)
    except:
        x = 0
        y = 0
        w = 0
        h = 0
    Bounding_Box = (x, y, w, h)

    print('Bounding_Box = ' + str(Bounding_Box))
    cv2.imshow('Mask', Mask)
    cv2.imshow('CM', Mask_closed)
    cv2.add(image, (-10, 100, -10, 0), dst=image, mask=Mask_closed)

    return centroid, Bounding_Box

def drawing(image, centroid, Bounding_Box):

    if centroid != (0, 0):

        # Drawing a cross
        x = centroid[0]
        y = centroid[1]
        w = 5
        h = 1
        cv2.rectangle(image, (x - w, y - h), (x + w, y + h), (0, 0, 255), 2)
        cv2.rectangle(image, (x - h, y - w), (x + h, y + w), (0, 0, 255), 2)

        # Drawing a Bounding_Box
        x1 = Bounding_Box[0]
        y1 = Bounding_Box[1]
        x2 = x1 + Bounding_Box[2]
        y2 = y1 + Bounding_Box[3]
        cv2.rectangle(image, (x1, y1), (x2, y2), (20, 100, 20), 2)

    else:

        image = image

    return image


def painting(screen, centroid, color, radius, shake_prevention):

    global coord_prev

    if centroid != (0, 0):

        coord = centroid

        try:
            distance = math.sqrt((coord[0] - coord_prev[0])**2 + (coord[1] - coord_prev[1])**2)
        except:
            distance = 150

        if coord_prev == (0,0) or (shake_prevention == 1 and distance >= 100):
            coord_prev = coord

        screen = cv2.line(screen, coord_prev, coord, color, radius)

        coord_prev = centroid

def main():
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('-j', '--json', type=str, required=True, help='Full path to json file')
    parser.add_argument('-usp', '--use_shake_prevention', type=str, required=True, help='Use shake prevention - Y or N')
    parser.add_argument('-um', '--use_mouse', type=str, required=True, help='Use your mouse to paint (color recognition is disabled) - Y or N')
    parser.add_argument('-s', '--screen', type=str, required=True, help='Pinting over a white screen(W), the video stream of the webcam (V) or an image(image path)')

    args = vars(parser.parse_args())

    # Read json file - limits
    file_name = args['json']
    with open(file_name, 'r') as json_file:
        range_of_limits = json.load(json_file)
    for x in range_of_limits:
        print("%s: %s" % (x, range_of_limits[x]))

    # Image
    capture = cv2.VideoCapture(0)
    cv2.namedWindow('Webcam', cv2.WINDOW_AUTOSIZE)
    _, image = capture.read()  # get an image from the camera
    print(image.shape)

    # Screen
    screen = np.ones(image.shape) * 255
    key = ord('k')
    radius = 5   # Initial radius for painting
    color = 0
    ScreenWindowName = 'Paint2.0'

    if args['use_shake_prevention'] == 'Y':
        shake_prevention = 1
    else:
        shake_prevention = 0

    if args['use_mouse'] == 'Y':
        use_mouse = 1
    else:
        use_mouse = 0

    while True:

        _, image = capture.read()  # get an image from the camera

        centroid, Bounding_Box = Masking(range_of_limits, image)

        image = drawing(image, centroid, Bounding_Box)

        screen, color, radius = KeyFunction(screen, key, color, radius)

        if args['screen'] == 'V':
            _, screen2 = capture.read()

            j, i, k = np.where(screen != [(255, 255, 255)])

            for a in range(0, len(j)):
                screen2[j[a], i[a], k[a]] = screen[j[a], i[a], k[a]]

            ScreenWindowName = 'Paint2.0 - Video Stream'

            cv2.imshow(ScreenWindowName, screen2)

        elif args['screen'] == 'W':
            cv2.imshow(ScreenWindowName, screen)

        else:
            screen2 = cv2.imread(args['screen'])
            screen2 = cv2.resize(screen2, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_CUBIC)

            j, i, k = np.where(screen != [(255, 255, 255)])

            for a in range(0, len(j)):
                screen2[j[a], i[a], k[a]] = screen[j[a], i[a], k[a]]

            ScreenWindowName = 'Paint2.0 - Image'

            cv2.imshow(ScreenWindowName, screen2)

        if use_mouse == 0:
            painting(screen, centroid, color, radius, shake_prevention)
        else:
            cv2.setMouseCallback(ScreenWindowName, partial(mouse_callback, screen=screen, color=color, radius=radius, shake_prevention=shake_prevention))

        cv2.imshow('Webcam', image)
        cv2.imshow('Paint2.0', screen)
        key = cv2.waitKey(20)
        print(key)

        if key == ord('w'):
            print('You pressed "w" (write). You saved the actual image!')
            screen_name = 'drawing_' + ctime() + '.png'
            cv2.imwrite(screen_name, screen)

        if key == ord('q'):
            print('You pressed "q" (quit). Program Finished!')
            break

if __name__ == '__main__':
    main()