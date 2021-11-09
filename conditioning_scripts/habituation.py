import time
import gpiozero as gz
import glob
import board
import RPi.GPIO as GPIO
import os
from picamera import PiCamera

start_time = time.time()

##Define solenoid outputs
##NOTE: Flipped logic for solenoid "on/off" switch##
clean_air = gz.DigitalOutputDevice(12)
clean_air.on()

##Define camera resolution and aperature
camera = PiCamera(resolution=(1920, 1080), framerate=30)
camera.iso = 1200

##Name session
project_folder = input("Project Name: ")
habituation_day = input("Habituation Day: ")
animal_ID = input("Animal ID: ")
trial_length = 600
trial_path = os.path.join("../drive_upload", project_folder, "habituation", habituation_day, animal_ID) 
video_recording = trial_path + ".h264" 

#Start video
camera.start_recording(video_recording)

###TRIAL STRUCTURE
while (time.time() - start_time) < trial_length:
    clean_air.off()

if (time.time() - start_time) >= trial_length:
    camera.stop_recording()

if (time.time()-start_time) == trial_length:
    print("I'm habituated, take me out!")

