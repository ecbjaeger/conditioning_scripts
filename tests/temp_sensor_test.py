from time import sleep, strftime, time
import board
import adafruit_pct2075
import os

i2c = board.I2C()  # uses board.SCL and board.SDA
pct = adafruit_pct2075.PCT2075(i2c)
temperature_filename = input("Temperature recording name: ")
temperature_pathname = os.path.join("../drive_upload", temperature_filename) 

print("Starting temperature recording")

with open(temperature_pathname, "a") as log:
	while True:
		temp = pct.temperature
		log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))
		sleep(1) 
