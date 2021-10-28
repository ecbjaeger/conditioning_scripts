import time
import numpy as np
import board
import busio
import adafruit_mlx90640

i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)

start_time = time.time()
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])

mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

def thermal_cam():
    frame = [1] * 768
    mlx.getFrame(frame)
    mean_temp = np.mean(frame)
    return(mean_temp)

reading_length = float(input("Reading Length: "))

while (start_time - time.time()) < reading_length:
    print(thermal_cam())
    time.sleep(1)
