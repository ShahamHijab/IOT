# Name: Shaham Hijab
# Reg:  22-NTU-CS-1373
# Home task: 2.1 Working with Neopixel and input button
print("starting of neopixel flashing ")

from machine import Pin
from neopixel import NeoPixel
import time

btn =Pin(0, Pin.IN, Pin.PULL_UP)    # same pin for physical esp32 s3 built in Boot buton
pin = Pin(48, Pin.OUT)              # set 48 for your physical esp32 s3  
neo = NeoPixel(pin, 1)              # create NeoPixel driver  for 1 pixel

colors = [(255,0,0),(0,255,0),(0,0,255)]
color_index = 0
press_count = 0

while True:
    if btn.value() == 0:
        press_count += 1
        print(f"Button pressed {press_count} times")
        
        while btn.value == 0:
            time.sleep(0.1)
            
        if press_count >= 5:
            press_count = 0       # Reset the press count
            color_index = (color_index + 1) % len(colors)  # Cycle through colors
            neo[0] = colors[color_index]
            neo.write()
            print(f"Color changed to: {colors[color_index]}")
    
    
    
    
#    while(btn.value()==1):          # flashing of neopixel stopped when button is in pressed status
#        neo[0] = (255, 0, 0)            # set the first pixel to red
#        print("red")
#    
#        neo.write()                     # write data to all pixels
#        time.sleep(.2)
#        neo[0] = (0, 255, 0)            # set the first pixel to green
#        print("red")
#    
#        neo.write()                     # write data to all pixels
#        time.sleep(.2)       
#        neo[0] = (0, 0, 255)            # set the first pixel to blue
#        print("blue")
#    
#        neo.write()                     # write data to all pixels
#        time.sleep(.2) 