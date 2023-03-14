#!/usr/bin/env python3

import argparse
import cv2
import numpy as np
from colorama import Fore, Style
import json
import os

window_name = 'Color Segmenter'


def onTrackbar(image, mode):
    # Reading Trackbars (High is equal or bigger than Low)
    Threshold_LOW_B_H = cv2.getTrackbarPos('LOW B/H', window_name)
    Threshold_HIGH_B_H = cv2.getTrackbarPos('HIGH B/H', window_name)
    if Threshold_HIGH_B_H < Threshold_LOW_B_H: # Condition that prevents a minimal input higher than the maximum input
        cv2.setTrackbarPos('HIGH B/H', window_name, Threshold_LOW_B_H)

    Threshold_LOW_G_S = cv2.getTrackbarPos('LOW G/S', window_name)
    Threshold_HIGH_G_S = cv2.getTrackbarPos('HIGH G/S', window_name)
    if Threshold_HIGH_G_S < Threshold_LOW_G_S:
        cv2.setTrackbarPos('HIGH G/S', window_name, Threshold_LOW_G_S)

    Threshold_LOW_R_V = cv2.getTrackbarPos('LOW R/V', window_name)
    Threshold_HIGH_R_V = cv2.getTrackbarPos('HIGH R/V', window_name)
    if Threshold_HIGH_R_V < Threshold_LOW_R_V:
        cv2.setTrackbarPos('HIGH R/V', window_name, Threshold_LOW_R_V)

    # Defining limits by mode (HSV or RGB)
    if mode == 0:

        print('\n\nNew threshold defined by:\n')
        print(Fore.BLUE + 'TH_B_min = ' + Style.RESET_ALL + str(
            Threshold_LOW_B_H) + Fore.BLUE + ', TH_B_max = ' + Style.RESET_ALL + str(Threshold_HIGH_B_H))
        print(Fore.GREEN + 'TH_G_min = ' + Style.RESET_ALL + str(
            Threshold_LOW_G_S) + Fore.GREEN + ', TH_G_max = ' + Style.RESET_ALL + str(Threshold_HIGH_G_S))
        print(Fore.RED + 'TH_R_min = ' + Style.RESET_ALL + str(
            Threshold_LOW_R_V) + Fore.RED + ', TH_R_max = ' + Style.RESET_ALL + str(Threshold_HIGH_R_V))

        range_of_limits = {'limits': {'B': {'min': Threshold_LOW_B_H, 'max': Threshold_HIGH_B_H},
                                      'G': {'min': Threshold_LOW_G_S, 'max': Threshold_HIGH_G_S},
                                      'R': {'min': Threshold_LOW_R_V, 'max': Threshold_HIGH_R_V}}}

        mins = np.array([range_of_limits['limits']['B']['min'], range_of_limits['limits']['G']['min'],
                         range_of_limits['limits']['R']['min']])
        maxs = np.array([range_of_limits['limits']['B']['max'], range_of_limits['limits']['G']['max'],
                         range_of_limits['limits']['R']['max']])

    else:

        print('\n\nNew threshold defined by:\n')
        print(Fore.CYAN + 'TH_H_min = ' + Style.RESET_ALL + str(
            Threshold_LOW_B_H) + Fore.CYAN + ', TH_H_max = ' + Style.RESET_ALL + str(Threshold_HIGH_B_H))
        print(Fore.MAGENTA + 'TH_S_min = ' + Style.RESET_ALL + str(
            Threshold_LOW_G_S) + Fore.MAGENTA + ', TH_S_max = ' + Style.RESET_ALL + str(Threshold_HIGH_G_S))
        print(Fore.LIGHTBLUE_EX + 'TH_V_min = ' + Style.RESET_ALL + str(
            Threshold_LOW_R_V) + Fore.LIGHTBLUE_EX + ', TH_V_max = ' + Style.RESET_ALL + str(Threshold_HIGH_R_V))

        range_of_limits = {'limits': {'H': {'min': Threshold_LOW_B_H, 'max': Threshold_HIGH_B_H},
                                      'S': {'min': Threshold_LOW_G_S, 'max': Threshold_HIGH_G_S},
                                      'V': {'min': Threshold_LOW_R_V, 'max': Threshold_HIGH_R_V}}}

        mins = np.array([range_of_limits['limits']['H']['min'], range_of_limits['limits']['S']['min'],
                         range_of_limits['limits']['V']['min']])
        maxs = np.array([range_of_limits['limits']['H']['max'], range_of_limits['limits']['S']['max'],
                         range_of_limits['limits']['V']['max']])

    # Creating Mask with limits defined
    Mask = cv2.inRange(image, mins, maxs)

    cv2.imshow(window_name, Mask)

    return range_of_limits


def main():
    # Parse inputs
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=int, required=True,
                        help='0 for processing with RGB or 1 for processing with HSV')
    args = vars(parser.parse_args())

    # Tracbars for image threshold
    min_threshold = 0
    max_threshold = 255

    cv2.namedWindow(window_name)
    cv2.createTrackbar('LOW B/H', window_name, min_threshold, max_threshold, onTrackbar)
    cv2.createTrackbar('HIGH B/H', window_name, min_threshold, max_threshold, onTrackbar)
    cv2.createTrackbar('LOW G/S', window_name, min_threshold, max_threshold, onTrackbar)
    cv2.createTrackbar('HIGH G/S', window_name, min_threshold, max_threshold, onTrackbar)
    cv2.createTrackbar('LOW R/V', window_name, min_threshold, max_threshold, onTrackbar)
    cv2.createTrackbar('HIGH R/V', window_name, min_threshold, max_threshold, onTrackbar)

    text_file_exist = False

    # Image
    capture = cv2.VideoCapture(0)
    cv2.namedWindow('Webcam', cv2.WINDOW_AUTOSIZE)

    while True:

        _, image = capture.read()  # get an image from the camera

        # Processing Mode
        mode = args['mode']
        if mode == 1:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        cv2.imshow('Webcam', image)
        range_of_limits = onTrackbar(image=image, mode=mode)
        key = cv2.waitKey(20)

        # Writing limits data in text file
        if key == ord('w'):
            text_file_exist = True
            file_name = 'limits.json'
            with open(file_name, 'w') as file_handle:
                print('You pressed "w" (write). Writing limits to file ' + file_name)
                json.dump(range_of_limits, file_handle)

        if key == ord('e'):
            print('You pressed "e" (exit). Program Finished!')
            break

        if key == ord('q'):
            print('You pressed "q" (quit). Program Finished without saving any limits!')
            if text_file_exist == True:
                os.remove('limits.json')
            break


if __name__ == '__main__':
    main()