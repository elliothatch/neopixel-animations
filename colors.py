from __future__ import division

import math
import time
import random
import argparse

import neopixel
from neopixel import Color

# LED strip configuration:
LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

def main():
    parser = argparse.ArgumentParser(description="Pretty colors on your neopixel strip!")
    parser.add_argument("--count", "-n", type=int, default=60, help="number of neopixels")
    parser.add_argument("--brightness", "-b", type=int, default=255, help="brightness of neopixels, 0-255")
    subparsers = parser.add_subparsers()

    resetParser = subparsers.add_parser("reset")
    resetParser.set_defaults(func=runReset)

    rainbowParser = subparsers.add_parser("rainbow")
    rainbowParser.set_defaults(func=runRainbow)

    burstParser = subparsers.add_parser("burst")
    burstParser.set_defaults(func=runBurst)

    args = parser.parse_args()

    # init neopixels
    pixels = neopixel.Adafruit_NeoPixel(args.count, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, args.brightness)
    # Intialize the library (must be called once before other functions).
    pixels.begin()

    args.func(pixels, args)

    return 0

def runReset(pixels, args):
    resetPixels(pixels)
    pixels.show()

def runRainbow(pixels, args):
    print ('Press Ctrl-C to quit.')
    while True:
        rainbowCycle(pixels)

def runBurst(pixels, args):
    print ('Press Ctrl-C to quit.')
    t = 0
    colorBurst = None
    colorBurst2 = None
    # colorParticle = ColorParticle(wheel(0), 30*2, pixels.numPixels()/2, 2, 0, 0.05)
    while True:
        if t%40 == 0:
            colorBurst = ColorBurst(random.randint(0,pixels.numPixels()-1), random.randint(0,255), 20, random.randint(20,35), 3, 0.05, 30/3, 30*1)
        if t == 0 or t%40 == 30:
            colorBurst2 = ColorBurst(random.randint(0,pixels.numPixels()-1), random.randint(0,255), 20, random.randint(20,35), 3, 0.05, 30/3, 30*1)
        colors = [0]*pixels.numPixels()
        setArrayValues(colors, colorBurst.simulate(t%40), False)
        setArrayValues(colors, colorBurst2.simulate((t-30)%40), False)
        # setArrayValues(colors, [colorParticle.simulate(t)], True)
        showColors(pixels, colors)

        t+= 1
        time.sleep(1/60)

def resetPixels(pixels):
    for i in range(pixels.numPixels()):
        pixels.setPixelColor(i, Color(0,0,0))

def getRed(color):
    return (color >> 16) & (2**16 - 1)

def getGreen(color):
    return (color >> 8) & (2**8 - 1)

def getBlue(color):
    return color & (2**8 - 1)

def getWhite(color):
    return (color >> 24) & (2**24 - 1)

def showColors(pixels, colors):
    for i in range(min(pixels.numPixels(), len(colors))):
        pixels.setPixelColor(i, colors[i])

    pixels.show()

def rainbowCycle(pixels, wait_ms=20):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256):
        for i in range(pixels.numPixels()):
            pixels.setPixelColor(i, wheel(((i * 256 / pixels.numPixels()) + j) & 255))
        pixels.show()
        time.sleep(wait_ms/1000.0)

class ColorBurst:
    def __init__(self, center, hue, hueVariance, particleCount, maxVelocity, maxDrag, minFadeTime, maxFadeTime):
        self.center = center
        self.hue = hue
        self.hueVariance = hueVariance
        self.maxVelocity = maxVelocity
        self.maxDrag = maxDrag
        self.minFadeTime = minFadeTime
        self.maxFadeTime = maxFadeTime

        self.rng = random.Random()
        self.particles = [ColorParticle(wheel(hue + int(self.rng.uniform(-hueVariance, hueVariance))), self.rng.uniform(minFadeTime, maxFadeTime), center, self.rng.uniform(-maxVelocity, maxVelocity),
            0, self.rng.uniform(0, maxDrag)) for i in range(particleCount)]

    def __repr__(self):
        return "{},{},{},{}".format(self.center, self.color, self.maxVelocity, self.fadeTime)

    # returns array of (index,color)
    def simulate(self, t):
        return [p.simulate(t) for p in self.particles]

class ColorParticle:
    def __init__(self, color, fadeTime, position, velocity, acceleration, drag):
        self.color = color
        self.fadeTime = fadeTime
        self.position = position
        self.velocity = velocity
        self.acceleration = acceleration
        self.drag = drag

    def __repr__(self):
        return "{},{},{},{}".format(self.color, self.position, self.velocity, self.drag)

    # returns (index, color)
    def simulate(self, t):
        # return (int(self.position + self.velocity*t + self.acceleration/2*t**2 -
            # (self.velocity*t**2)*self.drag*t),
            # 0),
        position = int(self.position + (self.velocity*(1/(1+self.drag*t)))*t)
        color = Color(0,0,0)
        if t >= 0:
            color = Color(max(0, int(lerp(getRed(self.color), 0, t/self.fadeTime))),
                max(0, int(lerp(getGreen(self.color), 0, t/self.fadeTime))),
                max(0, int(lerp(getBlue(self.color), 0, t/self.fadeTime))))
        return (position, color)

def lerp(a,b,t):
    return (b-a)*t + a

# takes array, and array of (index, value) and sets appropriately
def setArrayValues(arr, vals, wrap):
    for val in vals:
        if wrap or (val[0] >= 0 and val[0] < len(arr)):
            arr[val[0]%len(arr)] = val[1]

def makeColorBurst(pixels, center, color, maxVelocity, fadeTime, t):
    random.jumpahead
    colors = [0]*pixels.numPixels()
    # colors[(center t/fadeTime
    for j in range(strip.numPixels()):
        strip.setPixelColor((center+j)%strip.numPixels(), wheel((colorBegin + 5*j)%256))
        strip.setPixelColor((center-j)%strip.numPixels(), wheel((colorBegin + 5*j)%256))
        strip.show()
        time.sleep(wait_ms/1000.0)

    return colors



# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
	"""Wipe color across display a pixel at a time."""
	for i in range(strip.numPixels()):
		strip.setPixelColor(i, color)
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChase(strip, color, wait_ms=50, iterations=10):
	"""Movie theater light style chaser animation."""
	for j in range(iterations):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, color)
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    while pos < 0:
        pos += 255
    while pos > 255:
        pos -= 255
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

def rainbow(strip, wait_ms=20, iterations=1):
	"""Draw rainbow that fades across all pixels at once."""
	for j in range(256*iterations):
		for i in range(strip.numPixels()):
			strip.setPixelColor(i, wheel((i+j) & 255))
		strip.show()
		time.sleep(wait_ms/1000.0)

def theaterChaseRainbow(strip, wait_ms=50):
	"""Rainbow movie theater light style chaser animation."""
	for j in range(256):
		for q in range(3):
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, wheel((i+j) % 255))
			strip.show()
			time.sleep(wait_ms/1000.0)
			for i in range(0, strip.numPixels(), 3):
				strip.setPixelColor(i+q, 0)

def colorBursts(strip, wait_ms=10):
	for i in range(256):
		center = random.randint(0, strip.numPixels())
		colorBegin = random.randint(0, 256)
		for j in range(strip.numPixels()):
			strip.setPixelColor((center+j)%strip.numPixels(), wheel((colorBegin + 5*j)%256))
			strip.setPixelColor((center-j)%strip.numPixels(), wheel((colorBegin + 5*j)%256))
			strip.show()
			time.sleep(wait_ms/1000.0)

def networkPackets(strip, packets, delay_ms=500, wait_ms=30):
	while True:
		for packet in packets:
			networkPacket(strip, 0, packet, wait_ms=wait_ms)
			networkPacket(strip, 1, [Color(100,100,255)], wait_ms=wait_ms)
			time.sleep(delay_ms/1000.0)

def networkPacket(strip, direction, colors, wait_ms=15):
	for i in range(strip.numPixels() + len(colors)*2):
		resetPixels(strip)
		for j, color in enumerate(colors):
			idx = 0
			if direction == 0:
				idx = i-j - len(colors)
			else:
				idx = strip.numPixels() - (i-j - len(colors))
			if idx >= 0 and idx < strip.numPixels():
				strip.setPixelColor(idx, color)
		strip.show()

		time.sleep(wait_ms/1000.0)
	resetPixels(strip)
	strip.show()

	# while True:
		# GRB
		# colorBursts(strip)
		# packets = [
			# [Color(255,255,255)],
			# [Color(255,255,255)],
			# [Color(255,255,255), wheel(0)],
			# [Color(255,255,255), wheel(0), wheel(85)],
			# [Color(255,255,255), wheel(0), wheel(85), wheel(170)],
			# [Color(255,255,255), wheel(0), wheel(85), wheel(170), wheel(120)],
			# [Color(255,255,255), wheel(0), wheel(85), wheel(170), wheel(120), wheel(70)],
			# [Color(255,255,255), wheel(0), wheel(85), wheel(170), wheel(120), wheel(70)]
			# [Color(255,255,255)],
			# [Color(255,255,255)],
			# [Color(255,255,255)]
		# ]
		# networkPackets(strip, packets)
		# strip.show()
		# Color wipe animations.
		# colorWipe(strip, Color(255, 0, 0))  # Red wipe
		# colorWipe(strip, Color(0, 255, 0))  # Blue wipe
		# colorWipe(strip, Color(0, 0, 255))  # Green wipe
		# Theater chase animations.
		# theaterChase(strip, Color(127, 127, 127))  # White theater chase
		# theaterChase(strip, Color(127,   0,   0))  # Red theater chase
		# theaterChase(strip, Color(  0,   0, 127))  # Blue theater chase
		# Rainbow animations.
		# rainbow(strip)
		# rainbowCycle(strip)
		# theaterChaseRainbow(strip)

if __name__ == "__main__":
    main()

