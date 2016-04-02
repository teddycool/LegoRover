import os
import sys
import RPi.GPIO as GPIO

#import Sensors.RangeSensor_new_interrupt_based as RS

path = "/home/pi/send_data.fifo"
#os.mkfifo(path)  # TODO setup fifo file if needed

GPIO.setmode(GPIO.BCM)
#rs1 = RS.RangeSensor(GPIO, 23, 24)
fifo = open(path,"w")
fifo.write('hej')


