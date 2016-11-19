__author__ = 'brixterOne'


class Vision(object):

    def __init__(self, in_area, in_x, in_y, in_probability):
        self.area = in_area
        self.x = in_x
        self.y = in_y
        self.probability = in_probability

    def getArea(self):
        return  self.area