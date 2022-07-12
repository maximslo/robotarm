#import python modules needed to run script
import urx
import math
import numpy as np
import sys
import cv2
import csv
import time
import matplotlib
import matplotlib.pyplot as plt
import subprocess
#import math3d as m3d
# from findeliseoncamera import *

if __name__ == "__main__":

	"""Set up some initial parameters
	"""
	HOST = "192.168.91.128"
#	y, x, r = 92 , 92, 40
	y, x, r = 720 , 540, 10
	bounds = np.asarray([[-x, x], [-y, y], [-r,r]])
	#times to iterate over optimization scripts
	n_iter = 100
	#gradient descent related parameters
	rho = 0.9
	speed = 500
	#robot parameters l = length v- movement velocity in m/s a - acceleration
	l = 0.05
	v = 0.2
	a = 0.1
	r = 0.01

#optic pick location all of them the same, assuming all optics will be loaded
	mirror1 =  (-.3046, -.1227, 0.2, 3.145, 0, 0)
	mirror2 = mirror1
	mirror3 = mirror1
	positivelens = mirror1
	negativelens = mirror1

#optic placement locations
	#size in mm of optical component
	TCPmirror = 0.003
	TCPlargemirror = 0.004
	TCPneglens = 0.004
	TCPposlens= 0.0065
	#table misalignment offset
	shiftx = 0.001
	shifty = 0.00
	#optic placement locations
	mirror1set = (-.20475+ shiftx, .30264 + shifty, 0.115+TCPmirror, 2.902453, -1.20224, 0 )
	mirror2set = (-.20409+ shiftx, .36880 + shifty, 0.115+TCPlargemirror, 1.202235, 2.902453, 0 )
	mirror3set = (-.22971+ shiftx, .3688 + shifty, 0.115+TCPlargemirror, 1.202235, -2.90245, 0.00)
	negativelensset = (-.2289+ shiftx, .344 + shifty, 0.115+TCPneglens, 3.1415, 0, 0 )
	positivelensset = (-.2289+ shiftx, .29435 + shifty, 0.115+TCPposlens, 0, 3.1415, 0 )

#home positions
	robot_homeposition = (math.radians(0),
		math.radians(-90),
		math.radians(0),
		math.radians(-90),
		math.radians(0),
		math.radians(0.1))

	# The Joint position the robot starts at
	robot_startposition = (math.radians(-.3),
		math.radians(-120.8),
		math.radians(112),
		math.radians(-176.9),
		math.radians(-86),
		math.radians(0.84))

def donothing(objective, derivative, bounds,speed, n_iter, rho):
	"""A function that does nothing!
	"""
	return None

def objective(x,y,r):
	""" This is the minimization function for the lenses and mirrors to reach the center of the camera"""
	return [x**2 + y**2, math.pi*r*r]
 
# derivative of objective function
def derivative(x,y,r):
	""" 
	This is the gradient function which tells which direction the lenses or mirrors should go to bring the dot to the center of the camera.
	"""
	return np.asarray([2.0*x, 2.0*y, math.pi*2*r-62.8])
 

def LensMinimization(objective, derivative, bounds, speed , n_iter, rho, ep=1e-3):
	"""
	This function minimizes the pitch, yaw, and z distance of the lens to minimize the spot on the detector and put it in
	the center.
	"""
	#make some fake points to get algorithmn going
	radius = [100,90,80,70]
	slope =[(radius[-1]-radius[-4])/3]
	#thresh callback extracts the beam position from the camera. givin in [x,y,r] in pixels relative to center of camera
	solutions = list()
	solution = thresh_callback()
	#if cannot find beam repeat until it finds something with a radius larger than 5 pixels
	while solution[2] < 5:
		solution = thresh_callback()
	#gradient descent algorthim
	sq_grad_avg = [0.0 for _ in range(bounds.shape[0])]
	sq_para_avg = [0.0 for _ in range(bounds.shape[0])]
	for it in range(n_iter):
		gradient = derivative(solution[0], solution[1],solution[2])
		for i in range(gradient.shape[0]):
			sg = gradient[i]**2.0
			sq_grad_avg[i] = (sq_grad_avg[i] * rho) + (sg * (1.0-rho))
		new_solution = list()
		for i in range(solution.shape[0]):
			alpha = (ep + math.sqrt(sq_para_avg[i])) / (ep + math.sqrt(sq_grad_avg[i]))
			change = alpha * gradient[i]
			sq_para_avg[i] = (sq_para_avg[i] * rho) + (change**2.0 * (1.0-rho))
			value = solution[i] - change*speed
			new_solution.append(value)
		solution = np.asarray(new_solution)
		#translate lens in tool to base position
		t = robot.get_pose()
		robot.z_t -= 0.02
		if  slope[-1] < 0:
			t.pos.y -= solution[2]/500000
			print('move foward!', slope[-1])
		if slope[-1] == 0:
			print('not moving!', slope[-1])
		if slope[-1] > 0:
			t.pos.y += solution[2]/500000	
			print('move backwards!', slope[-1])
		t.pos.x -= solution[0]/5000000	
		t.pos.z += solution[1]/5000000
		robot.set_pose(t, vel = v/20, acc = a/20)
		time.sleep(2)
		solution = thresh_callback()
		radius.append(solution[2])
		slope.append((radius[-1]-radius[-5])/4)

		while solution[2] < 7:
			solution = thresh_callback()
		solutions.append(solution)
		solution_eval = objective(solution[0], solution[1], solution[2])
		print('>%d f(%s) = %.5f' % (it, solution, solution_eval[-2]))
		#if beam is within goal box, break the loop and proceed
		if 0 < abs(solution[0]) < 2:
			if 0 < abs(solution[1])  < 15:
				if 0 < abs(solution[2])  < 15:
					print(solution)
					break
	#save recorded data
	filename = 'Lensminimization.csv'
	with open(filename, 'w', newline='') as csvfile:  
		csvwriter = csv.writer(csvfile) 
		header = ['x','y','radius']
		csvwriter.writerow(header) 
		csvwriter.writerows(solutions)
		csvfile.close()	
	return solutions

def MirrorMinimization(objective, derivative, bounds, speed , n_iter, rho, ep=1e-3):
	"""
	This function minimizes the pointing of the beam to the center of the camera by modifying the pitch and yaw of the
	robotic arm around the TCP.
	"""
	#thresh callback extracts the beam position from the camera. givin in [x,y,r] in pixels relative to center of camera
	solutions = list()
	solution = thresh_callback()
	while solution[2] < 5:
		solution = thresh_callback()
	sq_grad_avg = [0.0 for _ in range(bounds.shape[0])]
	sq_para_avg = [0.0 for _ in range(bounds.shape[0])]
	for it in range(n_iter):
		gradient = derivative(solution[0], solution[1],solution[2])
		for i in range(gradient.shape[0]):
			sg = gradient[i]**2.0
			sq_grad_avg[i] = (sq_grad_avg[i] * rho) + (sg * (1.0-rho))
		new_solution = list()
		for i in range(solution.shape[0]):
			alpha = (ep + math.sqrt(sq_para_avg[i])) / (ep + math.sqrt(sq_grad_avg[i]))
			change = alpha * gradient[i]
			sq_para_avg[i] = (sq_para_avg[i] * rho) + (change**2.0 * (1.0-rho))
			value = solution[i] - change*speed
			new_solution.append(value)
		solution = np.asarray(new_solution)
		#rotate  robot in tool (TCP) around rz and ry
		robot.rz += solution[0]/500000
		robot.ry += solution[1]/500000
		time.sleep(1)
		solution = thresh_callback()
		while solution[2] < 4:
			solution = thresh_callback()
		solutions.append(solution)
		solution_eval = objective(solution[0], solution[1], solution[2])
		print('>%d f(%s) = %.5f' % (it, solution, solution_eval[-2]))
		#if beam position is within goal stop the loop
		if 0 < abs(solution[0]) < 2:
			if 0 < abs(solution[1])  < 2:
				print(solution)
				break
	#save data to file
	filename = 'mirrorminimization.csv'
	with open(filename, 'w', newline='') as csvfile:  
		csvwriter = csv.writer(csvfile) 
		header = ['x','y','radius']
		csvwriter.writerow(header) 
		csvwriter.writerows(solutions)
		csvfile.close()		

	return solutions

def mirrorplacement(inputs, output, optimize = 0):
	"""
	This function is supposed to move to make the UR robot move to the input location then run 	
	the specified optimization routine if specified. Otherwise write 0 for pick and place
	"""
	#translation up distance
	picktrans = (0,0,.05,0,0,0)
	placetrans = (0,0,.05,0,0,0)
	empty = (0,0,0,0,0,0)
	#the movements are as follows: go to pick up location, go down to pick up object, go back up, then go above place location, place the optic, once optimization is completed, go back above the place location
	movements = [inputs,inputs,inputs, output, output, output]
	translate = [picktrans, empty, picktrans ,placetrans,empty, placetrans]

	for i in range(len(movements)):
		robot.movel(np.add(movements[i], translate[i]), acc= a/2, vel = v/2, wait=False, relative=True)
		if i == len(movements)-5:
			input('Please place optic onto robotic arm!')
		#if the optic is being placed down, run optimization script
		if i == len(movements)-2:
			pathway = optimize(objective, derivative, bounds,speed, n_iter, rho)
			solutions = np.asarray(pathway)
			#Call user to accept that ground glass pillar is installed w/ glue. This is for cobot 			
			#functionality the software will later place the ground glass pillar by itself.
			input('Please press enter to continue AFTER placement of sapphire pillar with UV-15 epoxy!')

	#Call UV curing for 10 minutes
	#UVCure(600) # units in seconds

	return solutions

if __name__ == "__main__":
	#connect to robot
	do_wait = True
	if len(sys.argv) > 1:
		do_wait = False
	robot = urx.Robot(HOST)
	time.sleep(1)
	print("Connection Success!")
	robot.set_tcp((0, 0, .065, 0, 0, 0))
	robot.set_payload(1, (0, 0, 0.1))
	print("Initialization Success!")
	#do some sort of initialization and calibration steps.
	#calibrate() not yet implimented

	#take photo of optics on the table and determine if we have enough components and save position
	#input = ImageCapture()
	#raise Exception('Cannot find all optics!') if input != 4

	#move robot to initial poisition for alignment
	robot.movej(robot_startposition, vel = v, acc = a, wait=False)

	#automated pick place and alignment
	print("Starting Automated Optical Alignment, Please stand back!")
	inputs = [mirror1, mirror2, mirror3, positivelens, negativelens]
	output = [mirror1set, mirror2set,mirror3set, positivelensset, negativelensset]
	optimize = [donothing, donothing, MirrorMinimization, donothing, LensMinimization]
	#boundaries needed to make saved plots of visual recorded data
	xaxis = np.arange(bounds[0,0], bounds[0,1], 0.1)
	yaxis = np.arange(bounds[1,0], bounds[1,1], 0.1)
	xs, ys = np.meshgrid(xaxis, yaxis)
	#if you want to start at a specific optic
	startingoptic = int(input('Please specify which optic you want to start at! 1 = HR mirror; 2,3 is the DC mirrors; 4 is positive focal lens; and 5 is negative lens') or 1) -1
	for i in range(startingoptic, len(inputs)):
		solutions = mirrorplacement(inputs[i], output[i] , optimize[i])
		#mirrorplacement(inputs[i], output[i])
		if i == 2 or i == 4:
			#save heat map picture of recorded data
			plt.contourf(xs, ys, objective(xs,ys,r/10)[0], levels=50, cmap='jet')
			plt.scatter(solutions[:, 0], -solutions[:, 1], solutions[:,2]*10, color='w') 
			plots = plt.scatter(solutions[:, 0], -solutions[:, 1], solutions[:,2]*10, color='w') 
			names = [0,0,'MirrorMinimization', 0, 'LensMinimization']
			plots.figure.savefig( names[i] + '.png' , bbox_inches='tight')
			plt.clf()
	#go to home location
	robot.movej(robot_startposition, vel = v, acc = a, wait=False)

	time.sleep(2)

	#call the labview function to run M2 and automatically save results

	bashCommand = "iM2.exe savepath=\\ipgp-cd-fs01\Data\PicoLaser\Product_Docs\Green%20NLO%20Insertable%20Module\Production%20Test%20Data"
	process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
	output, error = process.communicate()

	time.sleep(2)

	#read saved results and populate the excel & PDB to complete.


	#Complete 
	robot.movej(robot_startposition, vel = v, acc = a, wait=False)
	robot.close()
	print('Success! Now place module under dragonlamp and complete')



