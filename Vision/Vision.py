__author__ = 'teddycool'
#Master class for the vision system, using other classes for each type of detection
#
#Webinfo used for this part of project:
# http://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android
import time
import sys
import cv2
import numpy as np
import argparse
from picamera import PiCamera
import picamera.array
from picamera.array import PiRGBArray
import os
try:
    from config import roverconfig
except:
    roverconfig = { "Streamer": {"StreamerImage": "/tmp/stream/pic.jpg", "StreamerLib": "/tmp/stream"},
                "Vision": {"WriteRawImageToFile": False, "WriteCvImageToFile": False},
                }
#from Logger import Logger
import SignFinder
import io


class Vision(object):
    test = False

    def __init__(self, resolution):
        time.sleep(2)
        print "Vision object started..."
        self._seqno = 0
        #self._log = Logger.Logger("Vision")
        self.white = cv2.imread('white.jpg', 0)
        self.cord_x = 0
        self.cord_y = 0
        self._lastframetime = 0
        if(not self.test):
            self._cam = PiCamera()
            self._cam.resolution = resolution
            self._cam.hflip = True
            self._cam.vflip = True
            self._cam.framerate = 10
            self._rawCapture = PiRGBArray(self._cam, size=resolution)
        self._center = (resolution[0]/2, resolution[1]/2)
        self.target_found = False

        print "Starting streamer..."
        print os.system('sudo mkdir /tmp/stream')
        print os.system('sudo LD_LIBRARY_PATH=/home/pi/mjpg-streamer/mjpg-streamer /home/pi/mjpg-streamer/mjpg-streamer/mjpg_streamer -i "input_file.so -f /tmp/stream -n pic.jpg" -o "output_http.so -w /home/pi/mjpg-streamer/mjpg-streamer/www" &')

        #TODO: check that streamer is running

    def initialize(self):
        print "Vision initialised"
        self._lastframetime = time.time()
        self.loopTime = 1
        if (not self.test):
            self._imagegenerator = self._cam.capture_continuous(self._rawCapture, format="bgr", use_video_port=True)

    def update(self):
        #self._log.info("Update started")
         #TODO: make threaded in exception catcher
        # https://picamera.readthedocs.org/en/release-1.10/recipes2.html#rapid-capture-and-processing
        if (not self.test):
            frame = self._imagegenerator.next()
            self._rawCapture.truncate()
            self._rawCapture.seek(0)
            self._frame = frame.array

        #if roverconfig["Vision"]["WriteRawImageToFile"]:
        #    cv2.imwrite("/home/pi/LegoRover/Imgs/camseq"+str(self._seqno)+".jpg",self._frame )

    def draw(self, frame):

        latest_loop_time = time.time()-self._lastframetime
        self.loopTime = (self.loopTime * 3 + latest_loop_time)/4
        print "Vision looptime: " + str(self.loopTime)
        self._lastframetime= time.time()

        # Mask out black color and turn the mask to an black and white picture
        mod_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        mod_frame = cv2.cvtColor(mod_frame, cv2.COLOR_GRAY2BGR)
        mod_frame = cv2.blur(mod_frame, (10, 10))
        self.hsv = cv2.cvtColor(mod_frame, cv2.COLOR_BGR2HSV)
        lower_black = np.array([0, 0, 0])
        upper_black = np.array([20,20,20])
        self.mask = cv2.inRange(self.hsv, lower_black, upper_black)
        self.res = cv2.bitwise_and(self.white, self.white, mask=self.mask)

        mask_size = cv2.countNonZero(self.mask)

        # Find regions of black and find their center coordinats
        (obj_contours, _) = cv2.findContours(self.res.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
        self.centres = []
        biggest_area = 0
        biggest_area_index = 0
        self.target_found = False
        for ind in range(len(obj_contours)):
            area = cv2.contourArea(obj_contours[ind])
            my_moments = cv2.moments(obj_contours[ind])
            my_centres = []
            if my_moments['m00'] != 0:
                my_centres.append(
                    (int(my_moments['m10'] / my_moments['m00']), int(my_moments['m01'] / my_moments['m00'])))
                cv2.circle(frame, my_centres[0], 10, (255, 255, 0), -1)

            if area < 1000:
                if area > biggest_area:
                    biggest_area = area
                    biggest_area_index = ind

        if biggest_area_index != 0:
            print biggest_area_index
            self.target_found = True
            self.centres = []
            obj_moments = cv2.moments(obj_contours[biggest_area_index])
            if obj_moments['m00'] != 0:
                self.centres.append((int(obj_moments['m10'] / obj_moments['m00']), int(obj_moments['m01'] / obj_moments['m00'])))
                self.xy = self.centres[0]
                print "Centers: " + str(self.xy)
                a = self.xy[0] - 320
                self.cord_x = a #4*self.cord_x/5 + a/5
                b = 240 - self.xy[1]
                self.cord_y = b #4 * self.cord_y/5 + b/5
                cv2.circle(frame, self.centres[0], 10, (55, 55, 0), -1)

        if self.target_found:
            print "Area size=" + str(biggest_area) + " x=" + str(self.cord_x) + " y=" + str(self.cord_y)
            cv2.putText(frame, "Area size: " + str(biggest_area) + " px", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2)
            cv2.putText(frame, "Target position x: " + str(a) + " y:" + str(b), (100, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2)
        else:
            print "No target found"
            cv2.putText(frame, "No target found", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (255, 255, 255), 2)

        cv2.putText(frame, "Mask size: " + str(mask_size) + " px", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imwrite("/home/pi/myproject/html/frame.jpg", frame)
        cv2.imwrite("/home/pi/myproject/html/res.jpg", self.res)

    def getCurrentFrame(self):
        return self._frame

    def getCurrentTargetX(self):
        return self.cord_x

    def getCurrentTargetY(self):
        return self.cord_y

    def getTargetFound(self):
        return self.target_found

    def __del__(self):
        print "Vision object deleted..."
        self._cam.close()

if __name__ == '__main__':
    print "Testcode for Vision"

    rgb_img = cv2.imread('cam.jpg')
    white = cv2.imread('white.jpg')

    hsv = cv2.cvtColor(rgb_img, cv2.COLOR_BGR2HSV)
    lower_red = np.array([30, 30, 30])
    upper_red = np.array([255, 255, 255])

    mask = cv2.inRange(rgb_img, lower_red, upper_red)
    res = cv2.bitwise_and(white, white, mask=mask)

    img = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    _, contours, _ = cv2.findContours(img.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_L1)
    print len(contours)

    centres = []
    biggest_area = 0
    biggest_area_index = 0
    for i in range(len(contours)):
        area = cv2.contourArea(contours[i])
        if area < 100:
            continue
        if area > biggest_area:
            biggest_area = area
            biggest_area_index = i

    if biggest_area_index != 0:
        moments = cv2.moments(contours[biggest_area_index])
        if moments['m00']!= 0:
            centres.append((int(moments['m10'] / moments['m00']), int(moments['m01'] / moments['m00'])))
            cv2.circle(rgb_img, centres[-1], 3, (255, 255, 0), -1)

        print "Area"
        print biggest_area
        print biggest_area_index

    cv2.imshow('image3', mask)
    cv2.imshow('image2', img)
    cv2.imshow('image', rgb_img)
   # cv2.imwrite('output.png', img)



    cv2.waitKey(0)

