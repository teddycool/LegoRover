__author__ = 'brixterOne'
#Handles the actual motors
from IMotionControl import IMotionControl
import os

class MotorControlLegoIr8884 (IMotionControl):

    def __init__(self, GPIO):
        super(MotorControlLegoIr8884, self).__init__()

    def setMotion(self, rotationspeed, frontSpeed):
        print "MotorControlLegoIr8884 setMotion..."
        leftWheelSpeed = frontSpeed - rotationspeed
        rightWheelSpeed = frontSpeed + rotationspeed

        # convert from WheelSpeed to hex commands
        os.system("sudo irsend SEND_ONCE LEGO_Combo_PWM 43A2") #Dummy value

        return

#
# if __name__ == '__main__':
#     print "Testcode for Driver"
#     import RPi.GPIO as GPIO
#     GPIO.setmode(GPIO.BCM)
#     import time
#     mc= MotorControlLegoIr8884(GPIO)
#     speed =100
#     mc.setSpeed(speed)
#     mc.forward()
#     while speed > 0:
#         time.sleep(3)
#         speed =speed - 10
#         mc.setSpeed(speed)
#         print mc.getCurrent()
#     mc.stop()
#     print mc.getCurrent()
#     GPIO.cleanup()
