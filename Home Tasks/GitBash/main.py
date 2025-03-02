#from machine import Pin
#from time import sleep

#btn = Pin(0, Pin.IN, Pin.PULL_UP)

#while TRUE:
 #   sleep(.4)
  #  print(btn.value())

# from machine import Pin
# from neopixel import NeoPixel
# import time

# pin = Pin(38, Pin.OUT)   # set GPIO48  to output to drive NeoPixel
# neo = NeoPixel(pin, 1)   # create NeoPixel driver on GPIO48 for 1 pixel
# neo[0] = (255, 0, 0) # set the first pixel to white
# time.sleep(.2)
# neo.write()              # write data to all pixels

from machine import Pin
from neopixel import NeoPixel
import time

pin = Pin(48, Pin.OUT)   # Set GPIO48 to output for NeoPixel
neo = NeoPixel(pin, 1)   # Create NeoPixel driver on GPIO48 for 1 pixel

colors = [(110, 220, 220),   # Red
          (0, 0, 0),   # Green
          (130, 340, 230)]   # Blue

while True:
    for color in colors:
        neo[0] = color  # Set the pixel to the current color
        neo.write()      # Write data to the NeoPixel
        time.sleep(0.3)  # Wait for 0.5 seconds before changing color