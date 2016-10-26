import math
import time
from networktables import NetworkTable
import cv2
import numpy as np
import os

os.system("uvcdynctrl -s 'Exposure, Auto' 1")
os.system("uvcdynctrl -s 'Exposure (Absolute)' 5")

import logging
logging.basicConfig(level=logging.DEBUG)

NetworkTable.setIPAddress('10.51.15.2')
NetworkTable.setClientMode()
NetworkTable.initialize()

nt = NetworkTable.getTable('pi')

cam = cv2.VideoCapture(0)
cam.set(3, 160);
cam.set(4, 120);

def rad(a):
	return math.pi * a / 180

def getAngle():
	#cam.open(0)
	ret, frame = cam.read()
	#ret, frame = cam.read()
	#cam.release()
	height, width, channels = frame.shape
	hsv = cv2.cvtColor(frame, cv2.COLOR_RGB2HSV)
	lower = np.array([0, 150, 50])
	upper = np.array([75, 255, 255])
	thresh = cv2.inRange(hsv, lower, upper)
	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	maxarea = 0
	centerx = 0
	contour = 0
	for c in contours:
		m = cv2.moments(c)
		if m['m00'] > maxarea:
			centerx = m['m10'] / m['m00']
			maxarea = m['m00']
			contour = c

	pixelOffset = width / 2 - centerx;
	angleOffset = 73 * pixelOffset / width
	angleOffset -= 3.5

	#x, y, w, h = cv2.boundingRect(contour)
	#w = float(w) / width
	#distance = math.cos(rad(64)) / (w * math.tan(rad(36.5)))

	print str(angleOffset)
	return angleOffset

while True:
	a = getAngle()
	if nt.isConnected() and a != 36 and a != 32.5:
		nt.putNumber('angletogoal', a)

