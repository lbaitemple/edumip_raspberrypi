import time
import datetime
from motor import Motor
from sensor.mpu6050 import MPU6050
from RotaryEncoder import  RotaryEncoder as Encoder
from remote.server import RemoteControlServer
from pid import PID
import settings


class Robot:
    def __init__(self):
        self.motor_left = Motor(settings.PINS['motor']['left'])
        self.motor_right = Motor(settings.PINS['motor']['right'])
        self.encoder_left = Encoder.Worker(settings.PINS['encoder']['left'])
        self.encoder_right = Encoder.Worker(settings.PINS['encoder']['right'])
        self.mpu = MPU6050(0x68)
        self.remote = RemoteControlServer(settings.pid_params)
        self.pid = PID()
        self.encoder_left.start()
        self.encoder_right.start()
    def run(self):
        self.remote.start()
        pwm_velocity = pwm_turn = 0
        counter_remote = counter_velocity = counter_turn = 0
        while True:
            begin_time = datetime.datetime.now()
            if self.remote.received['start']:
                self.mpu.update()
                pwm_balance = self.pid.get_balance_pwm(self.remote.received['pid']['balance'],
                                                       self.mpu.balance_angle + 1,
                                                       self.mpu.balance_gyro)
                if counter_velocity >= 2:
                    pwm_velocity = self.pid.get_velocity_pwm(self.remote.received['pid']['velocity'],
                                                             self.encoder_left.speed,
                                                             -self.encoder_right.speed,
                                                             self.remote.received['joystick'][0])
                    print(self.encoder_left.speed, self.encoder_right.speed)
                    self.encoder_left.speed = 0
                    self.encoder_right.speed = 0
                    counter_velocity = 0
                counter_velocity += 1

                if counter_turn >= 4:
                    pwm_turn = self.pid.get_turn_pwm(self.remote.received['pid']['turn'],
                                                     self.mpu.gyro['z'],
                                                     self.remote.received['joystick'][1])
                    counter_turn = 0
                counter_turn += 1

                # 小车倒下停车
                if self.mpu.balance_angle > 40 or self.mpu.balance_angle < -40:
                    self.pause()
                    self.remote.received['start'] = False
                    continue

                # 设置电机PWM
                pwm_left = int(pwm_balance + pwm_velocity + pwm_turn)
                pwm_right = int(pwm_balance + pwm_velocity - pwm_turn)
                self.motor_left.set_pwm(pwm_left)
                self.motor_right.set_pwm(pwm_right)

                # 发送远程数据，五个周期执行一次
                if counter_remote > 5:
                    self.remote.send_data(self.mpu.balance_angle,
                                          self.mpu.balance_gyro,
                                          self.mpu.turn_gyro,
                                          pwm_left,
                                          pwm_right)
                    counter_remote = 0
                counter_remote += 1
                if settings.DEBUG:
                    # print(self.mpu.gyro,self.mpu.accel)
                    print("PWM：%d,%d\t倾角：%f\t加速度%f" % (
                        pwm_left,
                        pwm_right,
                        self.mpu.balance_angle,
                        self.mpu.balance_gyro
                    ))
            else:
                self.pause()

            # 5毫秒执行一次主循环
            dt = (datetime.datetime.now() - begin_time).total_seconds()
            dt = (0.005 - dt) if dt < 0.005 else 0
            time.sleep(dt)

    def pause(self):
        self.motor_left.stop()
        self.motor_right.stop()

        self.encoder_left.reset()
        self.encoder_right.reset()

        self.pid.clean()

    def stop(self):
        self.motor_left.stop()
        self.motor_right.stop()
        self.encoder_left.cancel()
        self.encoder_right.cancel()

        self.mpu.close()


if __name__ == '__main__':
    my_robot = Robot()
    try:
        my_robot.run()
    except:
        my_robot.stop()
