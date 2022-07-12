import urx
import math
import numpy as np
import sys
import cv2
import csv
import time
from findeliseoncamera import *
import pandas

"""
The purpose of this program is to measure the beam stability, placement repeatability, and x,y,z yb,zb,xb accuracy of the robotic arm. Put in the pick up location and place location and radians, then it will output raw data that you can make into a graph of the resolution.
"""


if __name__ == "__main__":
	"""Set up some initial parameters
	"""
	HOST = "10.24.106.27"
	y, x, r = 92 , 92, 40
	bounds = np.asarray([[-x, x], [-y, y], [-r,r]])
	n_iter = 110
	rho = 0.99
	speed = 5

	l = 0.05
	v = 0.4
	a = 0.1
	r = 0.01

	robot_homeposition = (math.radians(0),
		math.radians(-90),
		math.radians(0),
		math.radians(-90),
		math.radians(0),
		math.radians(0.1))

	startposition =  (math.radians(3.33),
		math.radians(-90.25),
		math.radians(61.9),
		math.radians(-63.43),
		math.radians(-91.15),
		math.radians(5.83))

	setposition = (math.radians(-80.51),
		math.radians(-60.50),
		math.radians(84.70),
		math.radians(-113.38),
		math.radians(-87.66),
		math.radians(144))

def mirrorplacement(inputs, output, optimize = 0):
	"""
	This function is supposed to move to make the UR robot move to the input location. Otherwise write 0 for pick and place
	"""
	a = 0.1  # Robot acceleration value
	v = 0.4  # Robot speed value
	picktrans = (0,-0.1,-0.25,0.3,0,0)
	placetrans = (0,-0.1,-0.25,0.3,0,0)
	empty = (0,0,0,0,0,0)
	movements = [inputs,inputs,inputs, output, output,output]
	translate = [picktrans, empty, picktrans ,placetrans,empty, placetrans]
	for i in range(len(movements)):
		robot.movej(np.add(movements[i], translate[i]), acc= a, vel = v)
		if i == len(movements)-2:
			pathway = optimize(startposition,setposition, iter)
			solutions = np.asarray(pathway)
	return solutions

def wigglemeasure(inputs, output, iter):
	"""
	This function is supposed to slowly decrease movement in x,y,z, yb,zb,xb and measure the difference on the camera. Then output in file to later plot.
	"""
	print("Starting rotational and translational accuracy test!")
	beamdata=[]
	prebeamlocation = [0,0,0]
	postbeamlocation = [0,0,0]
	#initial step size
	zr = 1/1300
	t = robot.get_pose()
	movementlist = ['t.orient.rotate_xb(zr)',
			't.orient.rotate_yb(zr)', 
			't.orient.rotate_zb(zr)',
			'robot.translate_tool((zr, 0, 0), acc=a/2, vel=v/2)',
			'robot.translate_tool((0, zr, 0), acc=a/2, vel=v/2)']
	movementsay = [ 'xb','yb','zb','x','y']
	for i in range(len(movementlist)):
		for x in range(iter):
			time.sleep(5)
			print('moved!',movementsay[i])

			while prebeamlocation[2] == 0:
				prebeamlocation= thresh_callback()

			exec(movementlist[i])
			if x <2:
				robot.set_pose(t, vel = v/2, acc = a/2)
			time.sleep(5)

			while postbeamlocation[2] == 0:
				postbeamlocation = thresh_callback()

			robot.movej(setposition, vel = v, acc = a )
			t = robot.get_pose()
			difference = prebeamlocation - postbeamlocation
			print(str(i), x, difference)
			difference = list(difference)
			difference.insert(0,zr)
			difference.insert(0,x)
			difference.insert(0,movementsay[i])
			beamdata.append(difference)
			prebeamlocation = [0,0,0]
			postbeamlocation = [0,0,0]
			zr= zr/1.05
		zr = 1/1300

	filename = 'wigglemeasurements.csv'
	with open(filename, 'w', newline='') as csvfile:  
		csvwriter = csv.writer(csvfile) 
		header = ['movement type','int','step size','x diff','y diff','radius diff']
		csvwriter.writerow(header) 
		csvwriter.writerows(beamdata)
		csvfile.close()	

	return beamdata


def minrepeat(inputs, output, iter):
	"""
	This function is supposed to slowly decrease movement in x,y,z, yb,zb,xb and measure the difference on the camera. Then output in file to later plot.
	"""
	print("Starting rotational and translational accuracy test!")
	beamdata=[]
	prebeamlocation = [0,0,0]
	postbeamlocation = [0,0,0]
	#initial step size
	zr = 1/1300
	t = robot.get_pose()
	movementlist = ['t.orient.rotate_xb(zr)',
			't.orient.rotate_yb(zr)', 
			't.orient.rotate_zb(zr)',
			'robot.translate_tool((zr, 0, 0), acc=a/2, vel=v/2)',
			'robot.translate_tool((0, zr, 0), acc=a/2, vel=v/2)']
	movementsay = [ 'xb','yb','zb','x','y']
	for i in range(len(movementlist)):
		for x in range(iter):
			time.sleep(5)
			print('moved!',movementsay[i])

			while prebeamlocation[2] == 0:
				prebeamlocation= thresh_callback()

			exec(movementlist[i])
			if x <2:
				robot.set_pose(t, vel = v/2, acc = a/2)
			time.sleep(5)

			while postbeamlocation[2] == 0:
				postbeamlocation = thresh_callback()

			robot.movej(setposition, vel = v, acc = a )
			t = robot.get_pose()
			difference = prebeamlocation - postbeamlocation
			print(str(i), x, difference)
			difference = list(difference)
			difference.insert(0,zr)
			difference.insert(0,x)
			difference.insert(0,movementsay[i])
			beamdata.append(difference)
			prebeamlocation = [0,0,0]
			postbeamlocation = [0,0,0]

	filename = 'minrepeatmeasure.csv'
	with open(filename, 'w', newline='') as csvfile:  
		csvwriter = csv.writer(csvfile) 
		header = ['movement type','int','step size','x diff','y diff','radius diff']
		csvwriter.writerow(header) 
		csvwriter.writerows(beamdata)
		csvfile.close()	

	return beamdata


def pickplacerepeat(inputs, output, iter):
	"""
	This function is supposed to go back and forth between the pick and place position and record the beam position to measure repeatability from far locations.
	"""
	print("Starting pick and place repeatability test!")
	beamdata=[]
	a = 0.1  # Robot acceleration value
	v = 0.4  # Robot speed value
	picktrans = (0,-0.1,-0.25,0.3,0,0)
	placetrans = (0,-0.1,-0.25,0.3,0,0)
	empty = (0,0,0,0,0,0)
	beamlocation = [0,0,0]
	movements = [inputs,inputs,inputs, output, output,output]
	translate = [picktrans, empty, picktrans ,placetrans,empty, placetrans]
	for z in range(iter*2):
		for i in range(len(movements)):
			robot.movej(np.add(movements[i], translate[i]), acc= a, vel = v)
			if i == len(movements)-2:
				time.sleep(2)
				while beamlocation[2] == 0:
					beamlocation = thresh_callback()
				beamlocation = thresh_callback()
				time.sleep(2)
				beamlocation = list(beamlocation)
				beamlocation.insert(0,z)
				beamdata.append(beamlocation)
				print(beamlocation)
				beamlocation = [0,0,0]
				

	filename = 'picking_placing_repeatability.csv'
	with open(filename, 'w', newline='') as csvfile:  
		csvwriter = csv.writer(csvfile) 
		header = ['int','x pos','y pos','radius']
		csvwriter.writerow(header) 
		csvwriter.writerows(beamdata)
		csvfile.close()

	return beamdata

def beamstability(inputs,output,iter):
	"""
	This program will measure the stability of the arm to camera and provide a scatter of the x, y, radius measurements.
	"""
	print("Starting beam stability test!")
	beamdata=[]
	beamlocation = [0,0,0]
	for z in range(iter*10):
		while beamlocation[2] == 0:
			beamlocation = thresh_callback()
		time.sleep(2)
		beamlocation = list(beamlocation)
		beamlocation.insert(0,z)
		beamdata.append(beamlocation)
		print(beamlocation)
		beamlocation = [0,0,0]

	filename = 'beam_stability.csv'
	with open(filename, 'w', newline='') as csvfile:  
		csvwriter = csv.writer(csvfile) 
		header = ['int','x pos','y pos','radius']
		csvwriter.writerow(header) 
		csvwriter.writerows(beamdata)
		csvfile.close()


if __name__ == "__main__":
	robot = urx.Robot(HOST)
	print("Connection Success!")
	robot.set_tcp((0, 0, .068, 0, 0, 0))
	robot.set_payload(1, (0, 0, 0))
	print("Initialization Success!")

	iter= 100

	#beam stability measurement
#	mirrorplacement(startposition, setposition, beamstability)

	#wiggle measure data
#	mirrorplacement(startposition, setposition, wigglemeasure)

	#minrepeat measure data
#	mirrorplacement(startposition, setposition, minrepeat)

	#pick place measure data
	pickplacerepeat(startposition, setposition, iter)

	#Complete 
	robot.movej(startposition, vel = v, acc = a )
	robot.close()
	print('Success!')



