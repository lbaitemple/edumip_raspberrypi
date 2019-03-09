#!/usr/bin/python

from time import sleep

from lsm6ds33 import LSM6DS33

imu = LSM6DS33()
imu.enableLSM()

while True:
    print "Gyro:", imu.getComplementaryAngles(0.1)

    print "Accelerometer (G):", imu.getAccInG()
    sleep(2)
    print "Gyro Temperature:", imu.getTemperatureCelsius()
    sleep(0.1)
