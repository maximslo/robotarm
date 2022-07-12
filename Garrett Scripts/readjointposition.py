import urx
import math
import numpy as np
import sys
import cv2
import time
import subprocess
#import math3d as m3d
import ImageCapture, Calibrate

if __name__ == "__main__":

	"""Set up some initial parameters
	"""
	HOST = "10.24.106.27"
	speed = 5

	l = 0.05
	v = 0.9
	a = 0.5
	r = 0.01

def donothing(objective, derivative, bounds,speed, n_iter, rho):
	return None


if __name__ == "__main__":
	do_wait = True
	if len(sys.argv) > 1:
		do_wait = False
	robot = urx.Robot(HOST)
	print("Connection Success!")
	robot.set_tcp((0, 0, .10, 0, 0, 0))
	robot.set_payload(1, (0, 0, 0))
	print("Initialization Success!")

	print("Program to measure positions!")

	input('Please hold down free drive button to find first position then press enter!')
	t = robot.get_pos()
	print(t)
	t = robot.get_orientation()
	print(t)
	 
	robot.close()
	print('Success!')



