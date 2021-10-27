import time
import gpiozero as gz

relay = gz.DigitalOutputDevice(23)
solenoid = gz.DigitalOutputDevice(24)

relay.on()
time.sleep(5)
relay.off()

solenoid.on()
time.sleep(5)
solenoid.off()