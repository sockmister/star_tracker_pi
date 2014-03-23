import RPi.GPIO as GPIO
import time
import select
import sys

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
				exit

def calculate_angle(turns):
		return (-10**-18)*(turns)**3 + (20**-11)*(turns)**2 + 5*10**-5*(turns)

def sleep_for(difference):
		return (86164/360) * diff

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
				
				# elapsed = time.time() - start
				# print "elapsed: " + str(elapsed) + ", " + str(turns)

				GPIO.output(STEP, True)
				time.sleep(sleep_time/3)
				GPIO.output(STEP, False)

				turns += 1 
		else:
				for file in ready:
						line = file.readline()
						if not line:
								read_list.remove(file)
						elif line.rstrip():
								parse_commands(line)
