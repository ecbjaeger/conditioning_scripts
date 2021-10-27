import PID
import time
import os.path

from OmegaExpansion import AdcExp
from OmegaExpansion import pwmExp

pwmExp.setVerbosity(-1)
pwmExp.driverInit()
adc = AdcExp.AdcExp()

targetT = 35
P = 10
I = 1
D = 1

pid = PID.PID(P, I, D)
pid.SetPoint = targetT
pid.setSampleTime(1)

def readConfig ():
	global targetT
	with open ('/tmp/pid.conf', 'r') as f:
		config = f.readline().split(',')
		pid.SetPoint = float(config[0])
		targetT = pid.SetPoint
		pid.setKp (float(config[1]))
		pid.setKi (float(config[2]))
		pid.setKd (float(config[3]))

def createConfig ():
	if not os.path.isfile('/tmp/pid.conf'):
		with open ('/tmp/pid.conf', 'w') as f:
			f.write('%s,%s,%s,%s'%(targetT,P,I,D))
createConfig()

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


while 1:
	readConfig()
	#read temperature data
	temperature = read_temp()

	pid.update(temperature)
	targetPwm = pid.output
	targetPwm = max(min( int(targetPwm), 100 ),0)

	print ("Target: %.1f C | Current: %.1f C | PWM: %s %%"%(targetT, temperature, targetPwm)

	# Set PWM expansion channel 0 to the target setting
	pwmExp.setupDriver(0, targetPwm, 0)
	time.sleep(0.5)
