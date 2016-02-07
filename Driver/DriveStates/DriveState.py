__author__ = 'teddycool'
#Base for all DriveStates

class DriveState(object):

    def __init__(self, currentValues):
        return


    def initialize(self):
        #print "IMotionControl  setMotion"
        raise NotImplementedError

    def update(self, frame):
        return frame

    def draw(self, frame):
        return frame


if __name__ == '__main__':
    print "Testcode for "