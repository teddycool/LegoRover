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
        print "SignFinder initialize"
        self._hsvOrangeMin = np.array([1, 100, 100])
        self._hsvOrangeMax = np.array([2, 255, 255])
        self._hsvRedMin = np.array([160, 100, 100])
        self._hsvRedMax = np.array([179, 255, 255])
        self._hsvWhiteMin = np.array([0, 0, 100])
        self._hsvWhiteMax = np.array([255, 0, 255])
        self._hsvBlueMin = np.array([118, 100, 12])
        self._hsvBlueMax = np.array([122, 255, 255])

    def update(self, frame):
        frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        orange = cv2.inRange(frameHSV, self._hsvOrangeMin, self._hsvOrangeMax)
        red = cv2.inRange(frameHSV, self._hsvRedMin, self._hsvRedMax)
        blue = cv2.inRange(frameHSV, self._hsvBlueMin, self._hsvBlueMax)
        total_red = red#cv2.add(orange, red)
        self._stop = cv2.HoughCircles(total_red, cv2.cv.CV_HOUGH_GRADIENT, 3, 75, param1 = 100, param2 = 100, minRadius = 10, maxRadius = 75)
        return frame

    def draw(self, frame):
        if self._stop != None:
            self._stop = np.uint16(np.around( self._stop))
            print "Stops: " + str(len( self._stop))
            for i in  self._stop[0,:]:
                # draw the outer circle
                cv2.circle(frame, (i[0],i[1]), i[2], (0, 255, 0), 2)
                # draw the center of the circle
                cv2.circle(frame, (i[0],i[1]), 2, (0, 0, 255), 3)
        return frame

if __name__ == '__main__':
    print "Testcode for SignFinder"
    frame = cv2.imread("signtest1.jpg")
    sf = SignFinder()
    sf.initialize()
    sf.update(frame)
    sf.draw(frame)
    cv2.imshow("Sign", frame)
    cv2.waitKey(0)

