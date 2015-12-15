__author__ = 'teddycool'
#Purpose: to find traffic-signs in the delivered frame

import cv2
import numpy as np
import time

class SignFinder(object):

    def __init__(self):
        self._signs = {'Stop', 'Left', 'Right'}
        self._foundSigns = {}
        self._circles = None
        return


    def initialize(self):
        self._redLower = np.array([0, 20, 75], dtype = "uint8")
        self._redUpper = np.array([50, 60, 130], dtype = "uint8")
        return

    def update(self, frame):
        red = cv2.inRange(frame.copy(), self._redLower, self._redUpper)
        zeros = np.zeros(frame.shape[:2], dtype = "uint8")
        self._circles = cv2.HoughCircles(red,cv2.cv.CV_HOUGH_GRADIENT,1,50, param1=15,param2=15,minRadius=15,maxRadius=50)

    def draw(self, frame):
        if self._circles != None:
            print "Circles: " + str(len( self._circles))
            self._circles = np.uint16(np.around( self._circles))
            for i in  self._circles[0,:]:
                # draw the outer circle
                cv2.circle(frame,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(frame,(i[0],i[1]),2,(0,0,255),3)
        return frame


    def borders(self, img):
        redLower = np.array([0, 20, 75], dtype = "uint8")
        redUpper = np.array([50, 60, 130], dtype = "uint8")
        red = cv2.inRange(img.copy(), redLower, redUpper)
        zeros = np.zeros(img.shape[:2], dtype = "uint8")
        #For debug
        cv2.imshow("Red", red)
        circles = cv2.HoughCircles(red,cv2.cv.CV_HOUGH_GRADIENT,1,50, param1=15,param2=15,minRadius=15,maxRadius=50)

        if circles != None:
            print "Circles: " + str(len(circles))
            circles = np.uint16(np.around(circles))
            for i in circles[0,:]:
                # draw the outer circle
                cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
                # draw the center of the circle
                cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)
        return img


if __name__ == '__main__':
    print "Testcode for SignFinder"
    frame = cv2.imread("signtest1.jpg")
    sf = SignFinder()
    sf.initialize()
    sf.update(frame)
    sf.draw(frame)
    cv2.imshow("Sign", frame)
    cv2.waitKey(0)

