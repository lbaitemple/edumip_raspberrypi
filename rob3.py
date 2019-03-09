import time
import math
import datetime
from motor import Motor
from sensor.altimu import AltIMU
from RotaryEncoder import  RotaryEncoder as Encoder
from pid import PID
import settings
from sensor.mfilter import ModifiedFilter as Filter


class Robot:
    def __init__(self):
        self.motor_left = Motor(settings.PINS['motor']['left'])
        self.motor_right = Motor(settings.PINS['motor']['right'])
        self.encoder_left = Encoder.Worker(settings.PINS['encoder']['left'])
        self.encoder_right = Encoder.Worker(settings.PINS['encoder']['right'])
        self.pid = PID()
        self.mpu = AltIMU()
	self.mpu.enable()
	self.mpu.calibrateGyroAngles()
	self.mpu.initComplementaryFromAccel=True

        self.encoder_left.start()
        self.encoder_right.start()
	self.cstate={}
	self.cstate['theta']=0
	self.cstate['gamma']=0
	self.cstate['phi']=0
	self.cstate['wheelAngleR']=0
        self.cstate['wheelAngleL']=0


        self.setpoint={}
        self.setpoint['phi']=0
        self.setpoint['theta']=0
        self.setpoint['phidot']=0
        self.setpoint['gammadot']=0
	self.setpoint['gamma']=0

	self.D1 = Filter(0.01, settings.edumip_params['D1']['num'], settings.edumip_params['D1']['den'])
	self.D1.gain = settings.edumip_params['D1']['gain']
	self.D1.filter_enable_saturation(-1.0, 1.0)
	self.D1.filter_enable_soft_start(0.7)
	self.D1.name='D1'


	self.D2 = Filter(0.01, settings.edumip_params['D2']['num'], settings.edumip_params['D2']['den'])
	self.D2.gain = settings.edumip_params['D2']['gain']
	self.D2.filter_enable_saturation(-settings.edumip_params['D2']['theta_ref_max'], settings.edumip_params['D2']['theta_ref_max'])
	self.D2.filter_enable_soft_start(0.7)
        self.D2.name='D2'


	self.D3 = Filter()
	self.D3.filter_pid(settings.edumip_params['D3']['kp'], settings.edumip_params['D3']['ki'],
   	 	settings.edumip_params['D3']['kd'], 0.04, 0.01)
        self.D3.name='D3'


    def run(self):
        pwm_velocity = pwm_turn = 0
        counter_remote = counter_velocity = counter_turn = 0
	P=I=oldI=oldP=D=0
        bp=-60
        while True:
            begin_time = datetime.datetime.now()
            self.mpu.update(0.05,0)
	    theta = self.mpu.balance_angle+settings.BOARD_MOUNT_ANGLE*180/math.pi
	    print("---", theta, " : ", self.mpu.balance_roll)
	    roll = self.mpu.balance_roll*3.14/180
	    oldP = P
	    P=(roll) +bp
	    oldI = I
	    I = I + (P*0.05)
	    I = I + ((I-oldI)*2)
	    if (I> 250):
		I = 250
	    elif(I<-250):
		I = -250
	    D=P-oldP
	    pwm = P + I + D*10
	    if (pwm<0):  bp=bp-0.01
            if (pwm>0):  bp=bp+0.01

            dL=pwm
            dR=pwm
	    #print(dL, dR)

	    time.sleep(0.05)

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


if __name__ == '__main__':
    my_robot = Robot()
    try:
        my_robot.run()
    except:
        my_robot.stop()
