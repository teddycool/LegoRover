__author__ = 'teddycool'
#http://blog.miguelgrinberg.com/post/stream-video-from-the-raspberry-pi-camera-to-web-browsers-even-on-ios-and-android
import pygame
import pygame.camera
import picamera

class Cam(object):
    def __init__(self):
        print "Vision __init__"
        self.camid= 0
        self.width, self.height= (1024,768)


    def initialize(self):
        print "Vision initialize: " + str(self.camid)
        #Init and set up variables...
        pygame.camera.init()
        self.csnapshot = pygame.surface.Surface((self.width,self.height),0) #current frame
        self.psnapshot = pygame.surface.Surface((self.width,self.height),0) #previous frame
        self.cam = pygame.camera.Camera(self.camid,(self.width,self.height),"RGB")

    def update(self):
        #update each loop
        self.psnapshot = self.csnapshot
        self.csnapshot = self.cam.get_image(self.csnapshot)
        return self.csnapshot


    def draw(self, screen):
        #draw each loop
        return

if __name__ == "__main__":

    print pygame.surfarray.get_arraytype()
    import cv2
    import time
    cam=Cam()
    cam.initialize()
    snapshot = cam.update()
    #time.sleep(5)
    img=pygame.surface.Surface((cam.width,cam.height),0)
    t=0
    while 1:
        snapshot = cam.update()
        snapshot = pygame.transform.rotate(snapshot,90)
        snapshot = pygame.transform.flip(snapshot, 0, 1)
        img = pygame.surfarray.pixels3d(snapshot)
        cv2.imwrite('/temp/stream/pic.jpg',img,)
        #cv2.imshow('img',img)
        time.sleep(0.1)
        #http://docs.opencv.org/modules/core/doc/drawing_functions.html#puttext
        #cv2.putText(img,"Testing","Arial", 12,1,(250,250,250),2,None,None)

        #cv2.waitKey(0)
        #cv2.destroyAllWindows()