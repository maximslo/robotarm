from asyncio import sleep
from cmath import e
import urx
from urx import Robot
import math3d as m3d
import sys
import time
import math

# Connection and initial positions values
a = 0.5
v = 1.5

rob = Robot("192.168.91.128") 
rob.set_tcp((0, 0, 0.1, 0, 0, 0)) 
rob.set_payload(2, (0, 0, 0.1))

home = (math.radians(0),
		math.radians(-90),
		math.radians(0),
		math.radians(-90),
		math.radians(0),
		math.radians(0.1))

start = (math.radians(-.3),
		math.radians(-120.8),
		math.radians(112),
		math.radians(-176.9),
		math.radians(-86),
		math.radians(0.84))

mirrorHome = (math.radians(120),
			math.radians(-67),
			math.radians(88),
			math.radians(-110),
			math.radians(-91),
			math.radians(79))

time.sleep(0.2)  #leave some time to robot to process the setup commands
print("Initialization Success!")
print()

# Move to start position
rob.movej(mirrorHome, a, v, wait=False)

time.sleep(7)
# while True :
#     sleep(0.1)  #sleep first since the robot may not have processed the command yet
#     if not(rob.is_program_running()):
#         break

print("Robot is moving:", rob.is_program_running()) # For debuggging

# Snake Algorithm
print()
print("Starting snake path.")
# t = rob.getl()
# print(t)

# for x in range(1):
# 	snakePos = (math.radians(120),
# 				math.radians(-67),
# 				math.radians(88),
# 				math.radians(-110),
# 				math.radians(-91),
# 				math.radians(79)) #right
			
# 	rob.movel(snakePos, a, v, wait=False, relative=True)
# 	time.sleep(2)

# 	snakePos = (math.radians(120),
# 					math.radians(-67),
# 					math.radians(88),
# 					math.radians(-110-1),
# 					math.radians(-91), #up
# 					math.radians(79+4))

# 	rob.movej(snakePos, a, v, wait=False)
# 	time.sleep(2)

# 	snakePos = (math.radians(120),
# 					math.radians(-67),
# 					math.radians(88),
# 					math.radians(-110-1),
# 					math.radians(-91), 
# 					math.radians(79)) #left

# 	rob.movej(snakePos, a, v, wait=False)
# 	time.sleep(2)

# 	snakePos = (math.radians(120),
# 					math.radians(-67),
# 					math.radians(88),
# 					math.radians(-110-1-1),
# 					math.radians(-91), 
# 					math.radians(79)) 

# 	rob.movej(snakePos, a, v, wait=False)
# 	time.sleep(2)
# 	print("one cycle done")

# 	snakePos = (math.radians(120),
# 					math.radians(-67),
# 					math.radians(88),
# 					math.radians(-112),
# 					math.radians(-91), 
# 					math.radians(79+4)) 
			
# 	rob.movej(snakePos, a, v, wait=False)
# 	time.sleep(2)

# 	snakePos = (math.radians(120),
# 					math.radians(-67),
# 					math.radians(88),
# 					math.radians(-112-1),
# 					math.radians(-91), 
# 					math.radians(79+4))

# 	rob.movej(snakePos, a, v, wait=False)
# 	time.sleep(2)

# 	snakePos = (math.radians(120),
# 					math.radians(-67),
# 					math.radians(88),
# 					math.radians(-112-1),
# 					math.radians(-91), 
# 					math.radians(79)) #left

# 	rob.movej(snakePos, a, v, wait=False)
# 	time.sleep(2)

# 	snakePos = (math.radians(120),
# 					math.radians(-67),
# 					math.radians(88),
# 					math.radians(-112-1-1),
# 					math.radians(-91), 
# 					math.radians(79)) 

# 	rob.movej(snakePos, a, v, wait=False)
# 	time.sleep(2)
# 	print("two cycles done")

# print("Current x position is:", rob.x)
# print()
# storePosition = rob.getl()
# print("Current position is:")
# print(rob.getl())

# Works!
	# trans = rob.get_pose()
	# rob.x # returns current x
	# rob.rx # dumb
	# rob.rx -= 0.1 # rotate tool around X axis
	# rob.y_t += 0.1
rob.rx -= 0.3
# rob.translate((0.01, 0, 0), a, v, wait=False)


# rob.z_t += 0.01  # move robot in tool z axis for +1cm
# trans.pos.z += 0.01
# trans.orient.rotate_yb(0.01)
# rob.set_pose(trans, acc=0.5, vel=0.2)  # apply the new pose

# rob.z_t += 0.01

time.sleep(2)
# print("Robot is moving:", rob.is_program_running()) # For debuggging

# print()

# print("Position has changed:")
# print(not(storePosition == rob.getl()))
# print()
# print("Current position is:")
# print(rob.getl())

# rob.z_t += 0.04
	# rob.ry += 0.1
	# rob.rx -= 0.4
	# rob.ry += 0.1

# Move back to original pose.
val = input("Move back to home? (Y/N): ")
if val == 'Y':
	pass

rob.movej(home, a, v, wait=False)
time.sleep(6)

rob.stopj(a)
print("Program finished.")
sys.exit()