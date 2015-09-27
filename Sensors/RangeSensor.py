
import time
import cv2

class RangeSensor(object):
    
    def __init__(self, gpio, triggerpin=23, echopin=24):
        self._gpio = gpio
        self.TRIG = triggerpin
        self.ECHO = echopin
        self._lastrange = 0

        
        print "Distance Measurement initialized"
        
        self._gpio .setup(self.TRIG,self._gpio.OUT)
        self._gpio .setup(self.ECHO,self._gpio.IN)
        
        self._gpio .output(self.TRIG, False)
        print "Stabilizing rannge-sensor"
        time.sleep(2)

       
       
    def update(self):
        self._gpio.output(self.TRIG, True)
        time.sleep(0.00001) #Triggertime-high
        self._gpio.output(self.TRIG, False)
        pulse_start = time.time()
        while self._gpio.input(self.ECHO)==0:
          echo_start = time.time()
        
        while self._gpio.input(self.ECHO)==1:
          echo_end = time.time()
          
        pulse_duration_max = echo_end - pulse_start
        pulse_duration_min = echo_start - pulse_start
        pulse_duration = echo_end - echo_start
        #distance = high level time * sound-velocity (340M/S) / 2
        #dataspec suggest to use over 60ms measurement cycle, in order to prevent trigger signal to the echo signal. 
        distance_max = pulse_duration_max * 17000        
        distance_max = round(distance_max, 2)    
        distance_min = pulse_duration_min * 17000        
        distance_min = round(distance_min, 2) 
        distance = pulse_duration * 17000        
        distance = round(distance, 2)
        self._lastrange = distance
        print "RangeSensor: " + str(distance)
        return self._lastrange #_min, distance_max

    def draw(self, frame, textstarty):
        cv2.putText(frame, "Distance to object: " + str(self._lastrange) + " cm", (5,textstarty),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame



        
if __name__ == '__main__':
    print "Testcode for range sensor"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    rs = RangeSensor(GPIO)
    try:
        while 1:
            print rs.update()
            time.sleep(0.5)
    except:
        GPIO.cleanup()
