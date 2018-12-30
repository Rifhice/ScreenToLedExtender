import socket
import time
from neopixel import *
import argparse
import struct

# LED strip configuration:
LED_COUNT = 57      # Number of LED pixels.
LED_PIN = 18      # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN        = 10      # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
# True to invert the signal (when using NPN transistor level shift)
LED_INVERT = False
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--clear', action='store_true',
                    help='clear the display on exit')
args = parser.parse_args()

# Create NeoPixel object with appropriate configuration.
strip = Adafruit_NeoPixel(
    LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
# Intialize the library (must be called once before other functions).
strip.begin()

print ('Press Ctrl-C to quit.')
if not args.clear:
    print('Use "-c" argument to clear LEDs on exit')
try:
    socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.bind(('', 15555))

    socket.listen(5)
    client, address = socket.accept()
    print "{} connected".format(address)
    oldValues = ['0,0,0' for i in range(0,100)]
    while True:
	size = struct.unpack("i", client.recv(struct.calcsize("i")))[0]
        data = ""
        response = ""
	strip.setBrightness(64)
	while len(response) < size:
	    response = client.recv(size - len(data))
	print("new data")
	if response != "":
            splitted = response.split('|')[:-1]
	    leddone = [False for i in range(0,100)]
	    while not(leddone.count(True) == len(splitted)):
		for i, pixel in enumerate(splitted):
			r, g, b = pixel.split(',')
			oldR, oldG, oldB = oldValues[i].split(',')
			r = int(r)
			b = int(b)
			g = int(g)
			oldR = int(oldR)
			olgB = int(oldB)
			oldG = int(oldG)
			step = 5
			if not(int(oldR) == int(r)) or not(int(oldB) == int(b)) or not(int(oldG) == int(g)):
				newR = int(oldR)
				newB = int(oldB)
				newG = int(oldG)
				if int(r) < int(oldR):
					if abs(int(oldR) - int(r)) < step:
						newR = int(r)
					else:
						newR = newR - step
				elif int(r) > int(oldR): 
					if abs(int(r) - int(oldR)) < step:
                                                newR = int(r)
                                        else:
                                                newR = newR + step
				if int(g) < int(oldG):
                                        if abs(int(g) - int(oldG)) < step:
                                                newG = int(g)
                                        else:
                                                newG = newG - step
                       		elif int(g) > int(oldG):
                                        if abs(int(g) - int(oldG)) < step:
                                                newG = int(g)
                                        else:
                                                newG = newG + step
				if int(b) < int(oldB):
                                        if abs(int(b) - int(oldB)) < step:
                                                newB = int(b)
                                        else:
                                                newB = newB - step
                        	elif int(b) > int(oldB):
                                        if abs(int(b) - int(oldB)) < step:
                                                newB = int(b)
                                        else:
                                                newB = newB + step
				strip.setPixelColor(i, Color(int(newR), int(newG), int(newB)))
                		oldValues[i] = ','.join([str(newR), str(newG), str(newB)])
			else:
				leddone[i] = True
		strip.show()
except KeyboardInterrupt:
    if args.clear:
        colorWipe(strip, Color(0, 0, 0), 10)

print("Close")
client.close()
stock.close()
