import socket
import time
from neopixel import *
import argparse

# LED strip configuration:
LED_COUNT = 16      # Number of LED pixels.
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
    while True:
        response = client.recv(255)
        if response != "":
            print(response)
            splitted = response.split('|')[:-1]
            cpt = 0
            for pixel in splitted:
                r, g, b = pixel.split(',')
                strip.setPixelColor(cpt, Color(int(r), int(g), int(b)))
                strip.show()
                cpt = cpt + 1

except KeyboardInterrupt:
    if args.clear:
        colorWipe(strip, Color(0, 0, 0), 10)

print("Close")
client.close()
stock.close()
