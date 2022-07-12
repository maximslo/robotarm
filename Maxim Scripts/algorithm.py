# ALGORITHMS FOR UR3e ARM (must be in remote mode)
# by Maxim Slobodchikov during Summer 2022
# Note: if you encounter a "timeout error" on execution from Universal Robots, run again

from asyncio import sleep
from cmath import e
from urx import Robot
import math3d as m3d
import time
import math
import numpy as np
import matplotlib.pyplot as plt

# Power meter imports 
from datetime import datetime
from ctypes import cdll,c_long, c_ulong, c_uint32,byref,create_string_buffer,c_bool,c_char_p,c_int,c_int16,c_double, sizeof, c_voidp
from TLPM import TLPM
import time

# Sometimes cs majors forget physics exists
speed = 5
l = 0.05
v = 0.9
a = 0.5
r = 0.01

chip_height = 0.010 # 10mm tall
chip_width = 0.013 # 13mm across

def ccw_spiral(moves):
	# Function to return coordinates at Nth move of a counterclockwise square spiral.
	# Used for search if initial beam is off the meter.
	# Direction: right, up, left, down, repeat.
	x, y = 0, 0
	dx, dy = 0, -1 # the last move before our first move (going down before going left)
	counter = 0

	for n in range(np.inf):
		if((abs(x)==abs(y)) and [dx, dy] != [1, 0] or x>0 and y==1-x):
			dx = -dy # changes direction in ccw manner
			dy = dx
	
		counter += 1
		if counter == moves:
			return(x, y)

		x = x + dx
		y = y + dy
	
def powermeter():
	tlPM = TLPM()
	deviceCount = c_uint32()
	tlPM.findRsrc(byref(deviceCount))

	resourceName = create_string_buffer(1024)

	for i in range(0, deviceCount.value):
		tlPM.getRsrcName(c_int(i), resourceName)
		# print(c_char_p(resourceName.raw).value)
		break
	
	# print("\nPower meter connected.")
	tlPM.close()

	tlPM = TLPM()
	#resourceName = create_string_buffer(b"COM1::115200")
	#print(c_char_p(resourceName.raw).value)
	tlPM.open(resourceName, c_bool(True), c_bool(True))

	message = create_string_buffer(1024)
	tlPM.getCalibrationMsg(message)
	# print(c_char_p(message.raw).value)

	time.sleep(2)

	# power_measurements = []
	# times = []
	# count = 0
	# while count < 5:
	# 	power =  c_double()
	# 	tlPM.measPower(byref(power))
	# 	power_measurements.append(power.value)
	# 	times.append(datetime.now())
	# 	print(power.value)
	# 	count+=1
	# 	time.sleep(1)

	# Code to measure meter at any given moment
	power =  c_double()
	tlPM.measPower(byref(power))
	
	storage = power.value
	tlPM.close()
	return(storage)

def plot(x, y, halfmax):
	plt.title("Mirror Scan")
	plt.scatter(x, y, color='darkblue', marker='x')
	plt.plot(x, y)
	plt.axhline(y=halfmax, color='r', linestyle='-', label="halfmax")
	plt.xlabel("Shift from origin (mm)")
	plt.ylabel('Meter Readings (watts)')
	plt.grid(True)
	plt.legend()
	plt.show()

def h_scan():
	home() # Returns mirror to origin

	# Method to position beam in center of mirror by finding a horizontal and vertical edge and calculating middle.
	# Note: does not change TCP orientation/angle.

	# 1st: horizontal scan
	print("\nStarting horizontal scan...")
	print("(Mirror will be moving left)")
	hor_y = []
	hor_x = []
	left_mm = 0

	max = powermeter()
	halfmax = max/2
	print("Halfmax is:", halfmax, "watts")
	edge = False
	while(edge == False):
		measure = powermeter()

		print("Measure at", round(left_mm*1000, 0), "mm shift:", measure, "watts")
		hor_x.append(left_mm)
		hor_y.append(measure)

		rob.x_t += 0.001
		left_mm += 0.001
		
		if(measure<halfmax): # when beam overshoots edge, move back to find edge perfectly
			edge = True

	# Correcting overshoot and placing center of beam directly on edge
	# THIS DOESNT CENTER FOR SOME REASON
	hor_slope = (hor_y[-1]-hor_y[-2])/(hor_x[-1]-hor_x[-2])
	print(hor_slope)
	v_x = (halfmax - hor_y[-1] + hor_slope*hor_x[-1])/hor_slope
	print(v_x)
	rob.x_t -= v_x

	print("Horizontal scan finished")
	rob.x_t -= 0.0065 # We are at an edge, so move 1/2 of 13mm width back to center and stay
	plot(hor_x, hor_y, halfmax)
	
def v_scan():
	home()
	# 2nd: vertical scan (remember, we can only measure the top)
	print("\nStarting vertical scan...")
	print("(Mirror will be moving up)")
	vert_y = []
	vert_x = []
	down_mm = 0

	max = powermeter()
	halfmax = max/2
	print("Halfmax is:", halfmax, "watts")
	edge = False
	while(edge == False):
		measure = powermeter()

		print("Measure at", round(down_mm*1000, 0), "mm shift:", measure, "watts")
		vert_x.append(down_mm)
		vert_y.append(measure)

		rob.z_t += 0.001
		down_mm += 0.001
		
		if(measure<halfmax): # when beam overshoots edge, move back to find edge perfectly
			edge = True

	# Correcting overshoot and placing center of beam directly on edge
	vert_slope = vert_y[-1]-vert_y[-2]/vert_x[-1]-vert_x[-2]
	print(vert_slope)
	v_x = (halfmax - vert_y[-1] + vert_slope*vert_x[-1])/vert_slope

	rob.z_t -= v_x
	
	print("Vertical scan finished")
	rob.z_t -= 0.005 # We are at an edge, so move 1/2 of 10mm height back to center and stay

def test():
	print(powermeter())
	time.sleep(10)
	# To test movement accuracy
	# trans = rob.get_pose()  # get current transformation matrix (tool to base)
	# trans.pos.x += 0.01 # right
	# rob.set_pose(trans, acc=0.5, vel=0.2)

	# This moves along tool axis, which results in a tilted shift
	# print("right")
	rob.x_t -= 0.0005 # beam right
	rob.z_t -= 0.0005 # beam up
	# print("right")
	# rob.x_t -= 0.05
	# time.sleep(2)
	# home()
	print(powermeter())

def home():
	# Holds the home position of the arm, so you can easily call
	mirrorHome = (math.radians(59.83),
				math.radians(-76.68),
				math.radians(122.31),
				math.radians(-135.74),
				math.radians(-89.9),
				math.radians(16.83))
	rob.movej(mirrorHome, a, v, wait=True)

rob = Robot("10.0.0.10") # Used to connect to UR polyscope interface
print("\nConnection Success!")
# rob.set_tcp((0, -.003, .07, 0, 3.1416, 0))
# rob.set_payload(1, (0, 0, 0))
# print("Initialization Success!")

t = rob.getl() # Used to check position

h_scan()

rob.close()
print('\nProgram finished.')
