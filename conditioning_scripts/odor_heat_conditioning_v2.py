import time
import gpiozero as gz
import glob
import board
import RPi.GPIO as GPIO
import os
from picamera import PiCamera

start_time = time.time()

##Define solenoid outputs
clean_air = gz.DigitalOutputDevice(12)
odor = gz.DigitalOutputDevice(25)
clean_air.on()
odor.on()

##Define camera resolution and aperature
camera = PiCamera(resolution=(1920, 1080), framerate=30)
camera.iso = 1200

##Define start time and relay address
relay = gz.DigitalOutputDevice(23)
relay_status = 'off'

##Read temperature
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
    return temp_c

##Name session
project_folder = input("Project Name: ")
conditioning_day = input("Conditioning Day: ")
condition = input("Conditioning Type: ")
animal_ID = input("Animal ID: ")
trial_length = 420
end_time = (start_time + trial_length)
set_temp = 40
trial_path = os.path.join("../drive_upload", project_folder, "conditioning", conditioning_day, condition, animal_ID)
temperature_recording = trial_path + "_" + conditioning_day + ".csv" 
video_recording = trial_path + "_" + conditioning_day + ".h264" 

#Start video
camera.start_recording(video_recording)

###TRIAL STRUCTURE
with open(temperature_recording, "a") as log:
    while time.time()  < end_time:
        frame_number = camera.frame.index
        temp = read_temp()
        log.write("{0},{1}\n,{2}\n".format(time.strftime("%Y-%m-%d %H:%M:%S"),str(temp), str(frame_number)))
        time.sleep(0.01)
    
    #Trial phase 1: Only air, habituation
        if frame_number <= 1800:
            clean_air.off()
           # input_status == 'air'
    
    #Trial phase 2: Odor on, no heat
        if frame_number > 1800:
            clean_air.on()
            odor.off()
           # input_status == 'odor'
    
    #Trial phase 3: Odor and heat on until end of trial
        if temp < set_temp and relay_status == 'off' and frame_number >= 3600:
            relay.on()
            print("Relay on")
            relay_status == 'on'
            time.sleep(1)
            relay.off()
            print("Relay off")
            relay_status == 'off'
            time.sleep(1)
            print(read_temp())

        if frame_number >= 21000:
            camera.stop_recording()

        else:
            continue



