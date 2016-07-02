#This handles a set/list of rangesensors
#These sensors could not be activated at the same time but only one at a time to not interfere with each other
# rangsensordefinitions = [['channelname', triggerpin, echopin], ['channelname', triggerpin, echopin]....


import time
import cv2
import lcm
from LCM import usdistance


class RangeSensor(object):

    def __init__(self, gpio, rangesensordefinition):
        self._gpio = gpio
        self._gpio.setmode(self._gpio.BCM)
        self._channelName = rangesensordefinition[0]
        self._TRIG = rangesensordefinition[1]
        self._ECHO = rangesensordefinition[2]
        self._lastrange = 0
        self._history = []

        self._gpio.setup(self._TRIG,self._gpio.OUT)
        self._gpio.setup(self._ECHO,self._gpio.IN)

        self._gpio.output(self._TRIG, False)

        self._msg = usdistance.usdistance()
        self._msg.name = self._channelName
        self._msg.enabled = True

        print "Started range-sensor on pin: " + str(self._ECHO) + " for msg channel " + self._channelName

    def update(self):
        self._gpio.output(self._TRIG, True)
        time.sleep(0.01)  # Triggertime-high
        self._gpio.output(self._TRIG, False)
        pulse_start = time.time()
        echo_start = time.time()
        echo_end = time.time()
        # TODO: fix a timeout...
        while self._gpio.input(self._ECHO) == 0:
            echo_start = time.time()
            #if time.time() - pulse_start > 0.1:
            #    break

        while self._gpio.input(self._ECHO) == 1:
            echo_end = time.time()
            #if time.time() - pulse_start > 0.2:
            #    break

        pulse_duration_max = echo_end - pulse_start
        pulse_duration_min = echo_start - pulse_start
        pulse_duration = echo_end - echo_start
        # distance = high level time * sound-velocity (340M/S) / 2
        # dataspec suggest to use over 60ms measurement cycle, in order to prevent trigger signal to the echo signal.
        distance_max = pulse_duration_max * 17000
        distance_max = round(distance_max, 2)
        distance_min = pulse_duration_min * 17000
        distance_min = round(distance_min, 2)
        distance = pulse_duration * 17000
        distance = round(distance, 2)
        self._lastrange = distance
        self._msg.distance = self._lastrange
        #print "Lastrange: " + str(self._lastrange)

        #TODO: Fix history


class RangeSensorsLcm(object):
    
    def __init__(self, gpio, rangesensorlist):
        self._gpio = gpio
        self._gpio.setmode(self._gpio.BCM)
        self._rangeSensors = []
        for rangesensordef in rangesensorlist:
            self._rangeSensors.append(RangeSensor(self._gpio,rangesensordef)
            )
        self._lc = lcm.LCM()
        print "Stabilizing rangesensors...."
        time.sleep(2)

       
    def update(self):
        for range in self._rangeSensors:
           # print "Range update...   "
            range.update()
            self._lc.publish(range._channelName, range._msg.encode())
            print "Published distance RangeSensor for pin " + str(range._ECHO) + ": " + range._channelName + " -> " + str(range._msg.distance)
        time.sleep(0.2)



        
if __name__ == '__main__':
    print "RangeSensors runner started and will publish to LCM channels..."
    import lcm
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    rangsensors = RangeSensorsLcm(GPIO, [["RS1", 23,24],["RS2", 20,21]])
    try:
        while 1:
            rangsensors.update()
            time.sleep(0.1)

    except Exception as e:
        print str(e)
        GPIO.cleanup()