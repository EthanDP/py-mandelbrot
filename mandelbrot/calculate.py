from numba import jit
from serial import Serial
from time import sleep, time
import generate
import os

# Default values for calculations can be found in the
# start_gen function in the main.py project file.

serial_port = None
# Serial Codes
# 1 = Job Started
# 2 = Calculation Set Completed
# 3 = Job Completed

@jit
def calculate(x, y): # Self explanatory
	complex_value = complex(x, y)
	z = 0
	for i in range(128): # TODO: Change from hardcoded value
		z = z**2 + complex_value
		if z.real >= 2 or z.real <= -2:
			return i + 1
	return -1

def find_points(width, height, min_x, max_x, min_y, max_y):
	"""
	Calls the calculate() function on each point.

	Paramters:
	width, height: dimensions of the image/complex plane
	min_x, min_y: the minimum x and yi values for the plane
	max_x, max_y: the maximum x and yi values for the plane
	"""

	# TODO: Fix arduino job status indicator
	results_txt = open('results.txt', 'w+')
	
	write_serial(b'1')
	totalJobs = width * height
	write_serial(bytes(str(totalJobs), encoding="utf-8"))

	x_step = (max_x - min_x) / width
	y_step = (max_y - min_y) / height

	current_point = [min_x, min_y]
	x_point = 1
	y_point = 1
	while y_point <= height: # TODO: Fix precision issues (Perturbation or store in array)
		row = []
		while x_point <= width:
			point_result = calculate(*current_point)
			row.append(f"{point_result},{current_point[0]},{current_point[1]}")
			current_point[0] += x_step
			x_point += 1
		# TODO: Rewrite arduino progress indicator
		for point in row:
			results_txt.write(f"{point}\n")
		current_point[1] += y_step
		current_point[0] = min_x
		y_point += 1
		x_point = 1
	
	results_txt.close()
	write_serial(b'9')
	write_serial(b'x')
	generate.generate_image(int(width), int(height))
    
def write_serial(char_byte):
	"""
	Sends a byte to the specified serial port to be read
	by an arduino.

	Parameters:
	char_byte: the character to be sent, must be a bytes like object
	"""
	global serial_port
	if not serial_port:
		try:
			serial_port = Serial('/dev/ttyACM0', 9600)
			print("Found arduino")
			sleep(3) # Sleeps to give the arduino time to reset
		except:
			serial_port = 'x'
			print("Invalid port")
	if serial_port != 'x':
		serial_port.write(char_byte)
