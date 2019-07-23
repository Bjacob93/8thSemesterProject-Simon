#!/usr/bin/env python3
# NeoPixel library strandtest example
# Author: Tony DiCola (tony@tonydicola.com)
#
# Direct port of the Arduino NeoPixel library strandtest example.  Showcases
# various animations on a strip of NeoPixels.

import time
from neopixel import *
import argparse

def rgb_thing(strip):
	for i in range(0,30):
		if i%3 == 0:
			strip.setPixelColorRGB(i, 0, 0, 255)
			continue
		elif i%3 == 1:
			strip.setPixelColorRGB(i, 255, 0, 0)
			continue
		strip.setPixelColorRGB(i, 0, 255, 0)
		strip.show()

def theaterChase(strip, color, wait_ms=50, iterations=1):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(40):
            for i in range(0, strip.numPixels(), 30):
                strip.setPixelColor(i+q, color)
                strip.setPixelColor(i+q-1, Color(0, 230, 0))
                strip.setPixelColor(i+q-2, Color(0, 205, 0))
                strip.setPixelColor(i+q-3, Color(0, 180, 0))
                strip.setPixelColor(i+q-4, Color(0, 155, 0))
                strip.setPixelColor(i+q-5, Color(0, 130, 0))
                strip.setPixelColor(i+q-6, Color(0, 105, 0))
                strip.setPixelColor(i+q-7, Color(0, 80, 0))
                strip.setPixelColor(i+q-8, Color(0, 55, 0))
                strip.setPixelColor(i+q-9, Color(0, 30, 0))
                strip.setPixelColor(i+q-10, Color(0, 0, 0))
            strip.show()
            time.sleep(wait_ms/1000000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i+q, 0)
                strip.show()
            

strip = Adafruit_NeoPixel(30, 18, 800000, 5, False, 255)
strip.begin()

while True:
	theaterChase(strip, Color(0, 255, 0))
	break
