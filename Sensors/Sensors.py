__author__ = 'teddycool'
#Manage all sensors
import RangeSensor
import copy
import time
import config
import Compass
#import AccelGyro
import cv2


class Sensors(object):
    def __init__(self, GPIO):
        self._gpio = GPIO
        self.sensorvaluesdict={}
        valuesdict = {"Current": 0, "TrendList": []}
        sensors = ["UsFrontDistance", "Compass", "UsFrontRightDistance"] # ,"BarometricPressure", "Temperature", "Light", "Accelerometer", "Gyro","IrFrontDistance" ]
        for sensor in sensors:
            self.sensorvaluesdict[sensor]= copy.deepcopy(valuesdict)
        print "Created values dictionary..."
        self._rangeFwd=RangeSensor.RangeSensor(self._gpio,23,24)
        self._rangeRight = RangeSensor.RangeSensor(self._gpio,20,16)
        self._compass= Compass.Compass()

    def initialize(self):
        #connect each variable to the sensor and value
        self._compass.initialize()
        self._updateValues()


    def update(self):
         self._updateValues()

    def draw(self, frame):
        #Print sensorvalues to streamer lib for debug...
        frame = self._rangeFwd.draw(frame, 50)
        frame = self._rangeRight.draw(frame, 100)
        frame = self._compass.draw(frame, 150)
        return frame

    def _updateValues(self):
        #TODO: fix automatic update-call for each sensor -> .update()
        print "Updating sensor values started: " + str(time.time())
        self.sensorvaluesdict["UsFrontDistance"]["Current"] = self._rangeFwd.update()
        self.sensorvaluesdict["UsFrontRightDistance"]["Current"] = self._rangeRight.update()
        self.sensorvaluesdict["Compass"]["Current"] = self._compass.update()

        for key in self.sensorvaluesdict:
            self.sensorvaluesdict[key]["TrendList"] = self._updateValuesList(self.sensorvaluesdict[key]["Current"], self.sensorvaluesdict[key]["TrendList"] )
        print "Updating sensor values finished: " + str(time.time())

    def _updateValuesList(self,value, valuelist):
        if value != "N/A":
            valuelist.append(float(value))
            if (len(valuelist)> 10):
                poped = valuelist.pop(0)
        return valuelist

