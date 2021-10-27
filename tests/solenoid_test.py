import time
import gpiozero as gz

odor1 = gz.DigitalOutputDevice(12)
odor2 = gz.DigitalOutputDevice(25)

odor1.off()
time.sleep(5)

odor2.off()
time.sleep(5)
