import urx, math, sys


if __name__ == "__main__":

	"""Set up some initial parameters
	"""
	HOST = "192.168.91.128"
	l = 0.05
	v = 0.2
	a = 0.1
	r = 0.01

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


if __name__ == "__main__":
	do_wait = True
	if len(sys.argv) > 1:
		do_wait = False
	robot = urx.Robot(HOST)
	print("Connection Success!")
	robot.set_tcp((0, 0, .065, 0, 0, 0))
	robot.set_payload(1, (0, 0, 0.1))
	print("Initialization Success!")

	robot.translate_tool((0,0,-0.1), vel=v, acc=a)
	
	robot.movej(robot_startposition, vel = v, acc = a )
	robot.close()
	print('Success! Now place module under dragonlamp and complete')



