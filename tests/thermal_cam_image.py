import time, board, busio
import numpy as np
import adafruit_mlx90640
import matplotlib.pyplot as plt

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C communication
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
mlx_shape = (24,32)

# setup plot figure
plt.ion()
fig, ax = plt.subplots(figsize=(12,7))
therm1 = ax.imshow(np.zeros(mlx_shape), vmin=0, vmax=60) #initialize plot with zeros
cbar = fig.colorbar(therm1)
cbar.set_label('Temperature [$^{\circ}$C]', fontsize=14)

frame = np.zeros((24*32,))
t_array = []
while True:
    t1 = time.monotonic()
    try:
        mlx.getFrame(frame)
        data_array = (np.reshape(frame,mlx_shape))
        therm1.set_data(np.fliplr(data_array))
        therm1.set_clim(vmin=np.min(data_array), vmax=np.max(data_array))
        cbar.on_mappable_changed(therm1)
        plt.pause(0.001)
        fig.show()
        fig.savefig('../drive_upload/check_frame_size.png', dpi=300, facecolor='#FCFCFC', bbox_inches='tight')
        t_array.append(time.monotonic()-t1)
        print('Sample Rate: {0:2.1f}fps'.format(len(t_array)/np.sum(t_array)))
    except ValueError:
        continue
