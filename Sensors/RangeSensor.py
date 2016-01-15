
import time
import cv2

class RangeSensor(object):
    
    def __init__(self, gpio, triggerpin, echopin):
        self._gpio = gpio
        self.TRIG = triggerpin
        self.ECHO = echopin
        self._lastrange = 0

        
        print "Distance Measurement initialized for pin: " + str(echopin)
        
        self._gpio.setup(self.TRIG,self._gpio.OUT)
        self._gpio.setup(self.ECHO,self._gpio.IN)
        
        self._gpio.output(self.TRIG, False)
        print "Stabilizing range-sensor on pin: " + str(echopin)
        time.sleep(2)

       
    def update(self):
        self._gpio.output(self.TRIG, True)
        time.sleep(0.01) #Triggertime-high
        self._gpio.output(self.TRIG, False)
        pulse_start = time.time()
        echo_start = time.time()
        echo_end = time.time()
        #TODO: fix a timeout...
        while self._gpio.input(self.ECHO)==0:
            echo_start = time.time()
            if time .time() - pulse_start > 0.1:
                break
        
        while self._gpio.input(self.ECHO)==1:
            echo_end = time.time()
            if time .time() - pulse_start > 0.2:
                break
          
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
        print "Distance RangeSensor pin " + str(self.ECHO) + ": " + str(distance)
        return self._lastrange #_min, distance_max

    def draw(self, frame, name, textstartx, textstarty):
        cv2.putText(frame, name + ": " + str(self._lastrange) + " cm", (textstartx,textstarty),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)
        return frame



        
if __name__ == '__main__':
    print "Testcode for range sensor"
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    rs1 = RangeSensor(GPIO, 23, 24)
    rs2 = RangeSensor(GPIO, 20, 21)
    try:
        while 1:
            print "RS1: " + str(rs1.update())
            time.sleep(1)
            print "RS2: " + str(rs2.update())
            time.sleep(0.5)
    except Exception as e:
        print str(e)
        GPIO.cleanup()
