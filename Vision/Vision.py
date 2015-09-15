__author__ = 'teddycool'
#http://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android
import time
import picamera
import picamera.array
import cv2
import sys
import numpy as np
import LaserFinder
import ContourFinder
import os


class Vision(object):

    def __init__(self, resolution):
        print "Vision object started..."
        self._contourFinder = ContourFinder.ContourFinder()
        self._cam = picamera.PiCamera()
        self._cam.resolution = resolution
        self._center = (resolution[0]/2, resolution[1]/2)
        #TODO: check that streamer is running


    def initialize(self):
        self._cam.start_preview()


    def update(self):
        stream = picamera.array.PiRGBArray(self._cam)
        self._cam.capture(stream, format='bgr')
        # At this point the image is available as stream.array
        frame = stream.array
        self._contourFinder.update(frame)
        return frame

    def draw(self, frame):
        frame = self._contourFinder.draw(frame)
        #draw cross for center of image
        cv2.line(frame,(self._center[0]-20,self._center[1]),(self._center[0]+20, self._center[1]),(0,0,255),1)
        cv2.line(frame,(self._center[0],self._center[1]-20),(self._center[0],self._center[1]+20),(0,0,255),1)
        #cv2.line(frame, self._laserfinder._point, self._center,(0,255,0),2)

        #Draw to streamer lib to 'publish'
        #TODO: make threaded in exception catcher
        cv2.imwrite('/tmp/stream/pic.jpg',frame)
        #TODO: set up a defined framerate
        time.sleep(0.1)

    def __del__(self):
        print "Vision object deleted..."
        self._cam.close()




if __name__ == '__main__':
    print "Testcode for Vision"
    vision= Vision( (1024,768))
    vision.initialize()
    try:
        while 1:
            frame = vision.update()
            vision.draw(frame)
            time.sleep(0.2)
    except:
        e = sys.exc_info()[0]
        print e
