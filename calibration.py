import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

STEP = 17
DIR = 23
MOVE_SWITCH = 24

ONE_REV = 16 * 200 #16 microsteps * 200 steps 
REV_SPEED_FAST = 0.000001
REV_SPEED_SLOW = 0.0001 

MOVE_ONE_REV = 'm'
RESET = 'r'
PRINT = 'p'
HELP = 'h'
EXIT = 'q'

rev_count = 0

GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(MOVE_SWITCH, GPIO.IN)

GPIO.output(DIR, True)

HELP_STR = "Enter\nx: move x rev(s)\nr: reset\np: print rev_count\nh: help\nq: exit\n"
print HELP_STR

while(True):
		move = raw_input(">>> ")

		if(move.replace("-", "", 1).isdigit()):
				move = int(move)
				rev_count += move
				if(move < 0):
						GPIO.output(DIR, False)
						move *= -1
				else:
						GPIO.output(DIR, True)
				for i in range(move*ONE_REV):
						GPIO.output(STEP, True)
						time.sleep(0.000001)
						GPIO.output(STEP, False)

		if(move == RESET):
				if(rev_count < 0):
						GPIO.output(DIR, True)
				else:
						GPIO.output(DIR, False)
				for i in range(rev_count*ONE_REV):
						GPIO.output(STEP, True)
						time.sleep(0.000001)
						GPIO.output(STEP, False)
				rev_count = 0

		if(move == PRINT):
				print(rev_count)

		if(move == EXIT):
				print "warning: you should disconnect motor first to prevent it from moving."
				raw_input("enter to continue...")
				break

		if(move == HELP):
				print HELP_STR

GPIO.cleanup()

