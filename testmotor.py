from motor import Motor
import settings
import time
from RotaryEncoder import  RotaryEncoder as Encoder


motor_left = Motor(settings.PINS['motor']['left'])
motor_right = Motor(settings.PINS['motor']['right'])

while True:
    motor_left.set_pwm(100)
    motor_right.set_pwm(200)
    time.sleep(1)

    motor_left.stop()
    motor_right.stop()
    time.sleep(2)
