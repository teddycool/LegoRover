__author__ = 'teddycool'

# logic for driving...
# using MotorControlL298 and sensor values

import cv2
from MotorControl import MotorControlLegoIr8884


# from MotorControl import MotorControlL298



class Driver(object):
    def __init__(self, GPIO):
        self._gpio = GPIO
        # self._gpio.setmode(self._gpio.BCM)
        # self._mc = MotorControlL298.MotorControlL298(self._gpio)
        self._mc = MotorControlLegoIr8884.MotorControlLegoIr8884(self._gpio)
        self._drivemodes = ["FwdFast", "FwdSlow", "Stop", "RevFast", "RevSlow", "TRight", "TLeft"]
        self._driverStates = {}
        self.direction = ""
        # driverStateList = [" " ]
        return

    def initialize(self):
        self._mc.setMotion(0, 0)
        return

    def update(self, targetCoordinatesX, targetFound):
        if targetFound:
            if targetCoordinatesX < -200:
                self._mc.setMotion(10, 0)
                self.direction = "Turning left"
            elif targetCoordinatesX > 200:
                self._mc.setMotion(-10, 0)
                self.direction = "Turning right"
            else:
                self._mc.setMotion(0, 10)
                self.direction = "Moving forward"

        return

    def draw(self, frame, targetCoordinatesX, targetFound):
        cv2.putText(frame, self.direction, (100, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                            (255, 255, 255), 2)

        # cv2.putText(frame,"Speed: " + str(self._mc._currentSpeed) ,(5,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        #cv2.putText(frame, "Motor: " + str(self._mc._controlStates), (5, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
            #        (255, 255, 255), 2)

        return frame

    def __del__(self):
        self._mc.setMotion(0, 0)
        print "Driver object deleted..."
