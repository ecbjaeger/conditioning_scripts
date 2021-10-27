import time
import board
import adafruit_pct2075
i2c = board.I2C()
pct = adafruit_pct2075.PCT2075(i2c)

def C_to_F(C):
    return (C * 9/5) + 32

temp_count = 0
while temp_count < 5:
    print("Temperature: %.2f C\t %.2f F" % (pct.temperature, C_to_F(pct.temperature)))
    time.sleep(1)
    temp_count += 1