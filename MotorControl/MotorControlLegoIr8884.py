__author__ = 'brixterOne'
#Handles the actual motors
from IMotionControl import IMotionControl
import os
import math
import  time


class LegoCommand(object):

    def __init__(self, movement, duration):
        self.d = duration
        self.m = movement

    def getDuration (self):
        return self.d

    def getMovement(self):
        return self.m

class MotorControlLegoIr8884 (IMotionControl):

    def __init__(self, GPIO):
        super(MotorControlLegoIr8884, self).__init__()
        self._controlStates = {'LeftOn': True,'LeftRev': False, 'RightOn':True,  'RightRev': False}

    def irCommand(self, leftWheelSpeed, rightWheelSpeed):
        const_nible1 = 0x4

        ## configurable max rotation and front speeds
        c_MAX_ROT_SPEED = 5
        c_MAX_FRONT_SPEED = 10
        c_MAX_WHEEL_SPEED = c_MAX_FRONT_SPEED + c_MAX_ROT_SPEED
        c_MAX_WHEEL_HEX = 7

        leftWheelHEX = 0
        rightWheelHEX = 0
        lcr = 0

        ## transform right and left wheel speed to the Lego LIRC scale (mapping in excel)
        if leftWheelSpeed == 0:
            leftWheelHEX = 8
        elif leftWheelSpeed > 0:
            leftWheelHEX = int(math.ceil(float(leftWheelSpeed) / c_MAX_WHEEL_SPEED * c_MAX_WHEEL_HEX))
        else:
            leftWheelHEX = int(c_MAX_WHEEL_SPEED + math.ceil( float(leftWheelSpeed) / c_MAX_WHEEL_SPEED * c_MAX_WHEEL_HEX))


        ## left wheel motion is oposite due to the motor placement (mirrored)
        leftWheelHEX = 16 - leftWheelHEX

        if rightWheelSpeed == 0:
            rightWheelHEX = 8
        elif rightWheelSpeed > 0:
            rightWheelHEX = int(math.ceil( float(rightWheelSpeed) * c_MAX_WHEEL_HEX / c_MAX_WHEEL_SPEED))
        else:
            rightWheelHEX = int(c_MAX_WHEEL_SPEED + math.ceil(float(rightWheelSpeed) / c_MAX_WHEEL_SPEED * c_MAX_WHEEL_HEX))

        ## checksum calculation according to the pdf on LIRC
        lcr = 0xf ^ const_nible1 ^ rightWheelHEX ^ leftWheelHEX
        return "%1x%1x%1x%x" %(const_nible1, rightWheelHEX, leftWheelHEX, lcr)

    def setMotion(self, rotationspeed, frontSpeed):
        # print "MotorControlLegoIr8884 setMotion..."

        #frontSpeed = -frontSpeed
        rotationspeed = -rotationspeed

        ## calculate speed for each wheel according to the rotation and front speeds
        leftWheelSpeed = frontSpeed - rotationspeed
        rightWheelSpeed = frontSpeed + rotationspeed

        # rightWheelSpeed is oposite due to the motor placement
        rightWheelSpeed = -rightWheelSpeed

        # convert from WheelSpeed to hex commands
        irCMD = self.irCommand(leftWheelSpeed, rightWheelSpeed)
        os.system("sudo irsend SEND_ONCE LEGO_Combo_PWM %s" %irCMD)

        return



if __name__ == '__main__':
    print "Testcode for motor control IR"

    ctrl = MotorControlLegoIr8884(IMotionControl())

    ## test with user input on laptop
    # while True:
    #     rot = input("rotation speed:")
    #     front = input("front speed:")
    #
    #     front = -front
    #     leftWheelSpeed = front - rot
    #     rightWheelSpeed = front + rot
    #     irCMD = ctrl.irCommand(leftWheelSpeed, rightWheelSpeed)
    #
    #     print "rot %s,  front %s - %s " % (rot,front,irCMD)

    # test with user input on Pi
    #while True:
    #   rot = input("rotation speed:")
    #  front = input("front speed:")
    #  front = - front
    #  ctrl.setMotion(rot, front)

    def right():
        duration = 0.3
        while duration > 0:
            ctrl.setMotion(2, 0)
            time.sleep(0.1)
            duration = duration - 0.1
        return

    def left():
        duration = 0.3
        while duration > 0:
            ctrl.setMotion(-2, 0)
            time.sleep(0.1)
            duration = duration - 0.1
        return

    def stop():
        duration = 1
        while duration > 0:
            ctrl.setMotion(0, 0)
            time.sleep(0.1)
            duration = duration - 0.1
        return

    def forward():
        duration = 1
        while duration > 0:
            ctrl.setMotion(0, 3)
            time.sleep(0.1)
            duration = duration - 0.1
        return

    def backward():
        duration = 1
        while duration > 0:
            ctrl.setMotion(0,-3)
            time.sleep(0.1)
            duration = duration - 0.1
        return


    legoCommands = "FFHFVBBVFHHHHFFFVBBBBFFVFHBHBBVFFFFF"


    for lCommand in legoCommands:
        if lCommand == "H":
            right()
        if lCommand == "V":
            left()
        if lCommand == "S":
            stop()
        if lCommand == "F":
            forward()
        if lCommand == "B":
            backward()


