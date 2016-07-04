__author__ = 'teddycool'

import RPi.GPIO as GPIO

from Sensors import RangeSensorsLcm

GPIO.setmode(GPIO.BCM)
import time

print "Main sensor background loop for range sensors"

GPIO.setmode(GPIO.BCM)
rangsensors = RangeSensorsLcm.RangeSensorsLcm(GPIO, [["RS1", 23, 24], ["RS2", 20, 21]]) # rangsensordefinitions = [['channelname', triggerpin, echopin], ['channelname', triggerpin, echopin]....

try:
    while 1:
        rangsensors.update()
        time.sleep(0.1)
except Exception as e:
    print str(e)
    GPIO.cleanup()





