from picamera import PiCamera
from time import sleep
import os.path

camera = PiCamera(resolution=(1920, 1080), framerate=30)
camera.iso = 1200
projectname = input("Project ID: ")
filename = input("Name the video: ")
video_length = input("Video length (sec): ")
pathname = os.path.join('../drive_upload', projectname, filename)

camera.start_recording(pathname)
sleep(float(video_length))
camera.stop_recording()
