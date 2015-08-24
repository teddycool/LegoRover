import RPi.GPIO as GPIO
import time

class RangeSensor(object):
    
    def __init__(self, triggerpin=23, echopin=24):      
        GPIO.setmode(GPIO.BCM)
        
        self.TRIG = triggerpin 
        self.ECHO = echopin
        
        print "Distance Measurement initialized"
        
        GPIO.setup(self.TRIG,GPIO.OUT)
        GPIO.setup(self.ECHO,GPIO.IN)
        
        GPIO.output(self.TRIG, False)  
        print "Stabilizing rannge-sensor"
        time.sleep(2)
        
    def __del__(self):
        GPIO.cleanup()
       
       
    def Measure(self):
        GPIO.output(self.TRIG, True)
        time.sleep(0.00001) #Triggertime-high
        GPIO.output(self.TRIG, False)
        pulse_start = time.time()
        while GPIO.input(self.ECHO)==0:
          echo_start = time.time()
        
        while GPIO.input(self.ECHO)==1:
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
        return distance #_min, distance_max
        
        
if __name__ == '__main__':
    print "Testcode for range sensor"
    rs = RangeSensor()
    while 1:
        print rs.Measure()
        time.sleep(0.5)
