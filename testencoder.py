from motor import Motor
import settings
import time
from RotaryEncoder import  RotaryEncoder as Encoder


encoder_left = Encoder.Worker(settings.PINS['encoder']['left'])
encoder_right = Encoder.Worker(settings.PINS['encoder']['right'])
encoder_left.start()
encoder_right.start()

while True:
    print(encoder_left.speed, encoder_right.speed)
    time.sleep(1)
