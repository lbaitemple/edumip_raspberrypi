#from sensor.queue import Queue
from sensor.mfilter import ModifiedFilter as Filter
import settings
from sensor.lsm6ds3 import LSM6DS3 as MPU6050
import time

mpu = MPU6050(0x6b)

while True:
        time.sleep(0.5)
	mpu.update()
        print(mpu.getXRotation(), mpu.getYRotation(), mpu.getZRotation())
#	print(mpu.roll, mpu.pitch, mpu.heading, mpu.gyro, mpu.accel)

D1 = Filter(0.01, settings.edumip_params['D1']['num'], settings.edumip_params['D1']['den'])
D1.gain = settings.edumip_params['D1']['gain']
D1.filter_enable_saturation(-1.0, 1.0)
D1.filter_enable_soft_start(0.7)
D1.filter_print()


D2 = Filter(0.01, settings.edumip_params['D2']['num'], settings.edumip_params['D2']['den'])
D2.gain = settings.edumip_params['D2']['gain']
D2.filter_enable_saturation(-1.0, 1.0)
D2.filter_enable_soft_start(0.7)
D2.filter_print()

D3 = Filter()
D3.filter_pid(settings.edumip_params['D3']['kp'], settings.edumip_params['D3']['ki'],
    settings.edumip_params['D3']['kd'], 0.04, 0.01)
D2.filter_print()
