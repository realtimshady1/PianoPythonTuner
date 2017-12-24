#! /usr/bin/python

import pyaudio
import audioop
import RPi.GPIO as GPIO

FORMAT = pyaudio.paInt16# 2 Bytes
MAX_INT = 32768		# 2 ** 15 signed
CHANNELS = 1 		# Mono
RATE = 44100 		# Hertz
CHUNK = 1024 		# Number of values
PWM_PIN = 12		# Connect + to pin 12
DATA_SIZE = 2 		# Bytes 
FREQ = 50 		# Hertz
DUTY_CYCLE = 100	# Percent

audio = pyaudio.PyAudio()

# initialize modules
GPIO.setmode(GPIO.BOARD)
GPIO.setup(PWM_PIN, GPIO.OUT)
output = GPIO.PWM(PWM_PIN, FREQ)
output.start(0)

stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)



print "listening..."

try:
	while 1:
        	data = stream.read(CHUNK)
        	rms = audioop.rms(data, DATA_SIZE) * DUTY_CYCLE / MAX_INT
       		# print rms
		output.ChangeDutyCycle(rms)
except KeyboardInterrupt:
    print "finished recording"

output.stop()
GPIO.cleanup()
stream.stop_stream()
stream.close()
audio.terminate()

