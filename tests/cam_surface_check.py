import gpiozero as gz
import adafruit_mlx90640
import glob
import board
import RPi.GPIO as GPIO
import time
import os
import busio
import numpy as np

start_time = time.time()

##Read Pad Temperature
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.02)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
    return temp_c

##Read thermal cam temperature
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

def thermal_cam():
    frame = [1] * 768
    mlx.getFrame(frame)
    cam_temp = np.mean(frame)
    return(cam_temp)

##Name temperature recording
temperature_filename = input("Temperature recording name: ")
temperature_pathname = os.path.join("../drive_upload", temperature_filename) 
test_length = float(input("Test length: "))
set_temp = float(input("Set Temperature: "))

print("Starting temperature recording")

###Set GPIO Address for Heating Pad Relay
relay = gz.DigitalOutputDevice(23)
start_time = time.time()
relay_status = 'off'

##Write temperature file
pad_temp = read_temp()
camera_temp = thermal_cam()
with open(temperature_pathname, "a") as log:
    while (time.time() - start_time) < test_length:
        temp = read_temp()
        log.write("{0},{1}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(pad_temp), str(camera_temp))
        time.sleep(0.01)

##Ramp Up Temperature to set_temp at 1 sec intervals
        
        if temp < set_temp and relay_status == 'off':
            relay.on()
            print("Relay on")
            relay_status == 'on'
            time.sleep(1)
            relay.off()
            print("Relay off")
            relay_status == 'off'
            time.sleep(1)
            print(read_temp()) 
        
        elif temp >= (set_temp-0.5) and relay_status == 'on':
            relay.off()
            print("Maintaining Set Temp")
            print(read_temp())
            relay_status == 'off'
        
        else:
            continue
