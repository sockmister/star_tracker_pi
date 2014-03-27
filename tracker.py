import RPi.GPIO as GPIO
import time
import select
import sys
import math

GPIO.setmode(GPIO.BCM)

STEP = 17
DIR = 23

GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.output(DIR, True)

ONE_REV = 16 * 200

angle_i0 = 0
angle_i1 = 0
turns = 0
error_offset_adjustments = 0.00005
error_offset = error_offset_adjustments*2
DIFF_THRESHOLD = 0.0001

STOP = 0
START = 1
state = STOP

def parse_commands(line):
		if line == "s\n":
				if state == STOP:
						print "starting tracker..."
						state = START
				else:
						print "stopping tracker..."
						state = STOP

		if line == "r\n":
				print "resetting tracker..."
				global turns
				angle_i0, angle_i1 = 0, 0
				GPIO.output(DIR, False)
				for i in range(turns):
						GPIO.output(STEP, True)
						time.sleep(0.00001)
						GPIO.output(STEP, False)
				turns = 0
				GPIO.output(DIR, True)

		if line == "p\n":
				print "information:"
				print "micro_steps: " + str(turns)
				
		if line == "q\n":
				print "exiting..."
				raw_input("press enter to continue...")
				GPIO.cleanup()
				sys.exit()

def old_calculate_angle(turns):
		return (-10**-18)*(turns)**3 + (20**-11)*(turns)**2 + 5*10**-5*(turns)

def calculate_angle(turns):
		return (5*10**-18)*(turns)**3 + (1*10**-12)*(turns)**2 + (6*10**-5)*(turns) - 0.7136

def sleep_for(difference):
		return (86164/360) * diff

# how much earth has rotated
def earth_rotation(elapsed_time):
		return ((7.2921150*10**-5) * elapsed_time) * (180/math.pi)

read_list = [sys.stdin]
raw_input("press enter to start tracker.")
start = time.time()
while read_list:
		ready = select.select(read_list, [], [], 0)[0]
		
		if not ready:
				angle_i0 = angle_i1
				angle_i1 = calculate_angle(turns)
				diff = angle_i1 - angle_i0
				sleep_time = sleep_for(diff)
				
				elapsed = time.time() - start
				earth_curr_rotation = earth_rotation(elapsed)
				if turns % 1600 == 0:
						print "elapsed: " + str(elapsed) + ", " + str(turns) + ", " + str(sleep_time)
						print "earth_rotation: " + str(earth_curr_rotation) + " tracker angle: " + str(angle_i1)

				if (earth_curr_rotation - angle_i1) > DIFF_THRESHOLD:
						sleep_time -= error_offset
						error_offset += error_offset_adjustments
				else:
						if (error_offset > error_offset_adjustments):
							 error_offset -= error_offset_adjustments

				GPIO.output(STEP, True)
				time.sleep(sleep_time/2)
				GPIO.output(STEP, False)
				time.sleep(sleep_time/2)

				turns += 1 
		else:
				for file in ready:
						line = file.readline()
						if not line:
								read_list.remove(file)
						elif line.rstrip():
								parse_commands(line)
