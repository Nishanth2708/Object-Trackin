from picamera.array import PiRGBArray
import numpy as np
from picamera import PiCamera
import time
import datetime
from datetime import datetime
import cv2
from imutils.video import VideoStream
import imutils

camera = PiCamera()
camera.resolution = (1920, 1088)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(1920, 1088))

#Define the codec
today = time.strftime("%Y%m%d-%H%M%S")
fps_out = 32
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(today + ".avi", fourcc, fps_out, (1920, 1088))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

    image=frame.array
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Creating a Blank Canvas
    # blank = np.zeros(shape=[480, 480, 3], dtype=np.uint8)

    # Creating the Green HSV mask
    l_green = np.array([45, 60, 40])
    u_green = np.array([80, 255, 255])

    mask = cv2.inRange(hsv, l_green, u_green)
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.dilate(mask, kernel, iterations=3)

    # kernel1 = np.ones((3, 3), np.uint8)
    #
    # mask = cv2.erode(mask, kernel1, iterations=1)

    # mask=cv2.blur(mask,(5,5))
    # mask = cv2.resize(mask, (480, 480))
    bad = cv2.bitwise_and(frame, frame, mask=mask)

    # ret,thresh=cv2.threshold(mask,127,255,0)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    a = []

    for c in contours:

        arc_len = cv2.arcLength(c, True)
        area = cv2.contourArea(c)
        vertices = len(cv2.approxPolyDP(c, 0.01 * arc_len, True))
        # approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)

        M = cv2.moments(c)
        print(area)

        if vertices > 8 and area > 600:
            a.append(c)

        # if vertices>8 and M['m00']>150:
        #     a.append(c)
        # calculate x,y coordinate of center
        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        else:
            cX, cY = 0, 0
    for b in a:
        (x, y), rad = cv2.minEnclosingCircle(b)
        center = (int(x), int(y))
        # print(rad)
        rad = int(rad * 0.9)
        cv2.circle(frame, center, rad, (0, 0, 255), 2)
        cv2.circle(frame, center, 5, (255, 0, 0), -1)
        # print(a)
    # cv2.drawContours(frame, contours, -1, (0, 0, 255), 1)

    cv2.imshow('Masked', frame)
    cv2.imshow('y', bad)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
