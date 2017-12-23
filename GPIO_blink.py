#! usr/bin/python

# script to blink led on pin 12 on and off every second

import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)

p = GPIO.PWM(12, 1)
p.start(1)
raw_input('Press return to stop:')
p.stop()
GPIO.cleanup()
