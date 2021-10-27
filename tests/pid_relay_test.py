import PID
import time
import board
import os
import glob
import RPi.GPIO as gpio
#import adafruit_pct2075
import gpiozero as gz
import matplotlib.pyplot as plt

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
        sensor_temperature = float(temp_string) / 1000.0
    return sensor_temperature

##FOR PCT2075 TEMP SENSOR
#i2c = board.I2C()  # uses board.SCL and board.SDA
#sensor = adafruit_pct2075.PCT2075(i2c)

P = 1.4
I = 1
D = 0.045
pid = PID.PID(P, I, D)

pid.setPoint = 40
pid.setSampleTime(0.01)

total_sampling = 100
sampling_i = 0
measurement = 0
feedback = 0

relay = gz.DigitalOutputDevice(23)
# start_time = time.time()
relay_status = 'off'

temp_li = []
time_li = []
feedback_li = []
setpoint_li = []

try:
    while 1:
        pid.update(feedback)
        output = pid.output
        
        temperature = read_temp()
        if temperature is not None:
            if pid.SetPoint > 0:
                feedback += temperature + output
                
                print('i={0} desired.temp={1:0.1f}*C temp={2:0.1f}*C pid.out={3:0.1f} feedback={4:0.1f}'
                  .format(sampling_i, pid.SetPoint, temperature, output, feedback))
                
            if output > 0:
                print("heater on")
                relay.on()
                    
            elif output < 0:
                print("heater off")
                relay.off()

        if 0 < sampling_i >= 300:
            pid.SetPoint = 40

        time.sleep(0.5)
        sampling_i += 1
        
        feedback_li.append(feedback)
        setpoint_li.append(pid.SetPoint)
        temp_li.append(temperature)
        time_li.append(sampling_i)
        
        if sampling_i >= total_sampling:
            break

except KeyboardInterrupt:
    print("exit")
    relay.off()
    print("Heater off")

relay.off()
fig1 = plt.gcf()
fig1.subplots_adjust(bottom=0.15, left=0.1)

plt.plot(time_li, feedback_li, color ='red')
plt.plot(time_li, setpoint_li, color ='blue')
plt.xlim((0, total_sampling))
plt.ylim((min(feedback_li) - 0.5, max(feedback_li) + 0.5))
plt.xlabel('time (s)')
plt.ylabel('PID (PV)')
plt.title('Temperature PID Controller')


fig1.savefig('../drive_upload/pid_temperature.png', dpi=100)


