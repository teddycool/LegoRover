__author__ = 'teddycool'
#Handles the actual motors


class IMotionControl(object):
    def __init__(self):
        print "ISensor init..."

    def getValue(self):
        raise NotImplementedError