import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

STEP = 17
DIR = 23

GPIO.setup(STEP, GPIO.OUT)
GPIO.setup(DIR, GPIO.OUT)

ONE_REV = 16 * 200

angle_i = 0
angle_i1 = 0
turns = 0

while(True):
		angle_i = angle_i1
		# y = -1E-18x3 + 2E-11x2 + 5E-05x
		angle_i1 = (-10**-18)*(turns)**3 + (20**-11)*(turns)**2 + 5*10**-5*(turns)
		diff = angle_i1 - angle_i
		#  86164 / 360 * diff
		sleep_time = (86164/360) * diff

		GPIO.output(STEP, True)
		time.sleep(sleep_time)
		GPIO.output(STEP, False)

		turns += 1 
