__author__ = 'brixterOne'
#Handles the actual motors
from IMotionControl import IMotionControl
import os
import math

class MotorControlLegoIr8884 (IMotionControl):


    def __init__(self, GPIO):
        super(MotorControlLegoIr8884, self).__init__()

    def setMotion(self, rotationspeed, frontSpeed):
        print "MotorControlLegoIr8884 setMotion..."
        leftWheelSpeed = frontSpeed - rotationspeed
        rightWheelSpeed = frontSpeed + rotationspeed

        # convert from WheelSpeed to hex commands
        os.system("sudo irsend SEND_ONCE LEGO_Combo_PWM 43A2") #Dummy value to be changed

        return

    def irCommand(leftWheelSpeed,rightWheelSpeed):
        const_nible1 = 4
        c_MAX_ROT_SPEED = 5
        c_MAX_FRONT_SPEED = 10
        c_MAX_WHEEL_SPEED = c_MAX_FRONT_SPEED
        c_MAX_WHEEL_HEX = 7

        leftWheelHEX = 0
        rightWheelHEX = 0

        if leftWheelSpeed == 0:
            leftWheelHEX = 8
        elif leftWheelSpeed > 0:
            leftWheelHEX = math.ceil(float(leftWheelSpeed)/c_MAX_WHEEL_SPEED) * c_MAX_WHEEL_HEX
        else:
            leftWheelHEX = 16 - math.ceil(float(leftWheelSpeed)/c_MAX_WHEEL_SPEED) * c_MAX_WHEEL_HEX

