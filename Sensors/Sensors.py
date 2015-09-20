__author__ = 'teddycool'
#Manage all sensors
import RangeSensor
import copy
import time
import config
import Compass
import AccelGyro
import cv2


class Sensors(object):
    def __init__(self):
        self.sensorvaluesdict={}
        valuesdict = {"Current": 0, "TrendList": []}
        sensors = ["UsFrontDistance", "IrFrontDistance",]
        for sensor in sensors:
            self.sensorvaluesdict[sensor]= copy.deepcopy(valuesdict)
        print "Created values dictionary..."
        self._rangeFwd=RangeSensor()

    def initialize(self):
        #connect each variable to the sensor and value
        self._updateValues()


    def update(self):
         self._updateValues()

    def draw(self, frame):
        #Print sensorvalues to streamer lib for debug...
        return

    def _updateValues(self):
        print "Updating sensor values started: " + str(time.time())
        self.sensorvaluesdict["UsFrontDistance"]["Current"] = self._rangeFwd.Meassure()

        for key in self.sensorvaluesdict:
            self.sensorvaluesdict[key]["TrendList"] = self._updateValuesList(self.sensorvaluesdict[key]["Current"], self.sensorvaluesdict[key]["TrendList"] )
        print "Updating sensor values finished: " + str(time.time())

    def _updateValuesList(self,value, valuelist):
        if value != "N/A":
            valuelist.append(float(value))
            if (len(valuelist)> 10):
                poped = valuelist.pop(0)
        return valuelist

