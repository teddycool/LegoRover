__author__ = 'teddycool'

import cv2
import numpy as np

class ContourFinder(object):

    def __init__(self):
        return


    def initialize(self):
        return

    def update(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        edged = cv2.Canny(blurred, 30, 150)
        (self._cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2 .CHAIN_APPROX_SIMPLE)

    def draw(self, frame):
        if self._cnts:
            cv2.drawContours(frame, self._cnts, -1, (0, 255, 0), 2)
        return frame

if __name__ == '__main__':
    print "Testcode for ContourFinder"
    frame = cv2.imread("pic.jpg")
    cf = ContourFinder()
    frame = cf.update(frame)
    cf.draw(frame)
    cv2.imshow("Contours", frame)
    cv2.waitKey(0)
