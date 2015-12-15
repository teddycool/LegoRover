__author__ = 'teddycool'

#logic for driving...
#using MotorControl and sensor values

import MotorControl
import cv2

class Driver(object):


    def __init__(self, GPIO):
        self._gpio = GPIO
        self._mc = MotorControl.MotorControl(self._gpio)
        self._drivemodes = ["FwdFast", "FwdSlow", "Stop", "RevFast", "RevSlow", "TRight", "TLeft"]
        return

    def initialize(self):
        self._mc.stop()
        return

    def update(self, sensorvaluesdict):
        print "Driver update"
        if sensorvaluesdict["UsFrontLeftDistance"]["Current"] > 50 and sensorvaluesdict["UsFrontRightDistance"]["Current"] > 50:
            self._mc.forward()
            self._mc.setSpeed(100)

        if sensorvaluesdict["UsFrontLeftDistance"]["Current"] < 30 and sensorvaluesdict["UsFrontRightDistance"]["Current"] > 50:
            self._mc.rightTurn()
            self._mc.setSpeed(50)

        if sensorvaluesdict["UsFrontLeftDistance"]["Current"] > 50 and sensorvaluesdict["UsFrontRightDistance"]["Current"] < 30:
            self._mc.leftTurn()
            self._mc.setSpeed(50)

        if sensorvaluesdict["UsFrontLeftDistance"]["Current"] < 10 or sensorvaluesdict["UsFrontRightDistance"]["Current"] < 10:
            self._mc.reverse()
            self._mc.setSpeed(50)

        return

    def draw(self, frame):
        cv2.putText(frame,"Speed: " + str(self._mc._currrentSpeed) ,(5,40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        cv2.putText(frame,"Motor: " + str(self._mc._controlStates),(5,60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

        return frame

    def __del__(self):
        self._mc.stop()
        print "Driver object deleted..."
