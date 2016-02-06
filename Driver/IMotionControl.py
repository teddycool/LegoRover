

__author__ = 'teddycool'
#Handles the actual motors


class IMotionControl(object):
    def __init__(self):
        print "IMotionControl init..."

    def setMotion(self, rotationspeed, frontSpeed):
        raise NotImplementedError