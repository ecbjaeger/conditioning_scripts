import gpiozero as gz
import board
import adafruit_pct2075
import time
import os

i2c = board.I2C()  # uses board.SCL and board.SDA
pct = adafruit_pct2075.PCT2075(i2c)
curr_temp = pct.temperature

while True:
    print(curr_temp)