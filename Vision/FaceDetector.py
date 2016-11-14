__author__ = 'psk'
import cv2

class FaceDetector(object):

	def __init__(self):
		# load the face detector
		self.faceCascade = cv2.CascadeClassifier("cascades/haarcascade_frontalface_default.xml")
	def initialize(self,scaleFactor= 1.1 , minNeighbors= 5, minSize=(50, 50) ,flags=cv2.CASCADE_SCALE_IMAGE ):
		self._sf = scaleFactor
		self._mn = minNeighbors
		self._ms= minSize
		self._flags = flags

	def update(self, frame):
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		self._faceRects = self.faceCascade.detectMultiScale(gray, scaleFactor= self._sf  , minNeighbors= self._mn, minSize=self._ms ,flags=self._flags)

	def draw(self, frame):
		for (fX, fY, fW, fH) in self._faceRects:
			cv2.rectangle(frame, (fX, fY), (fX + fW, fY + fH), (0, 0, 255), 2)
		return frame



if __name__ == '__main__':
	print "Testcode for FaceDetector"
	frame = cv2.imread("_K3_5414.jpg")
	fd = FaceDetector()
	fd.initialize()
	fd.update(frame)
	fd.draw(frame)
	cv2.imshow("Faces", frame)
	cv2.waitKey(0)
