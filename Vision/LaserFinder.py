__author__ = 'teddycool'

import cv2
import numpy as np

class LaserFinder(object):

    def __init__(self):
        self._point = (100,100)


    def initialize(self):
        self._laserLower = np.array([230, 220, 230], dtype = "uint8")
        self._laserUpper = np.array([255, 250, 255], dtype = "uint8")

    def update(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        img = cv2.medianBlur(gray,5)
        circles = cv2.HoughCircles(img,cv2.cv.CV_HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=2,maxRadius=30)
        if circles != None:
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
                cv2.putText(frame, str((i[0],i[1])), (i[0],i[1]),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
                self._point = (i[0],i[1])

    def draw(self, frame):
        cv2.circle(frame,(self._point),2,(0,0,255),3)
        cv2.putText(frame, str(self._point), (self._point),cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 2)
        return frame

