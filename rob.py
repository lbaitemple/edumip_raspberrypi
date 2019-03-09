import time
import datetime
from motor import Motor
from sensor.altimu import AltIMU
from RotaryEncoder import  RotaryEncoder as Encoder
from pid import PID
import settings
from sensor.mfilter import ModifiedFilter as Filter

DT=0.1
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
        self.setpoint['phidot']= settings.DRIVE_RATE_ADVANCED
        self.setpoint['gammadot']=settings.TURN_RATE_ADVANCED
	self.setpoint['gamma']=0

	self.D1 = Filter(DT, settings.edumip_params['D1']['num'], settings.edumip_params['D1']['den'])
	self.D1.gain = settings.edumip_params['D1']['gain']
	self.D1.filter_enable_saturation(-1.0, 1.0)
	self.D1.filter_enable_soft_start(0.7)
	self.D1.name='D1'


	self.D2 = Filter(DT, settings.edumip_params['D2']['num'], settings.edumip_params['D2']['den'])
	self.D2.gain = settings.edumip_params['D2']['gain']
	self.D2.filter_enable_saturation(-settings.edumip_params['D2']['theta_ref_max'], settings.edumip_params['D2']['theta_ref_max'])
	self.D2.filter_enable_soft_start(0.7)
        self.D2.name='D2'


	self.D3 = Filter()
	self.D3.filter_pid(settings.edumip_params['D3']['kp'], settings.edumip_params['D3']['ki'],
   	 	settings.edumip_params['D3']['kd'], 4*DT, DT)
        self.D3.filter_enable_saturation(-settings.STEERING_INPUT_MAX, settings.STEERING_INPUT_MAX)

        self.D3.name='D3'


    def run(self):
        pwm_velocity = pwm_turn = 0
        counter_remote = counter_velocity = counter_turn = 0
        while True:
            begin_time = datetime.datetime.now()
            self.mpu.update(DT,0)
	    theta = self.mpu.balance_angle
            self.cstate['theta']=self.mpu.balance_angle*3.14/180+settings.BOARD_MOUNT_ANGLE
	    self.cstate['wheelAngleR']=self.encoder_right.speed*2*3.14/2130
            self.cstate['wheelAngleL']=self.encoder_left.speed*2*3.14/-2130
	    self.cstate['phi']= (self.cstate['wheelAngleR']+ self.cstate['wheelAngleL'])/2+self.cstate['theta']
            self.cstate['gamma']= (self.cstate['wheelAngleR']-self.cstate['wheelAngleL'])*(settings.WHEEL_RADIUS_M/settings.TRACK_WIDTH_M)
	    self.d2_u=self.D2.filter_march(self.setpoint['phi']-self.cstate['phi'])
	    self.setpoint['theta']=self.d2_u
            self.d1_u=self.D1.filter_march(self.setpoint['theta']-self.cstate['theta'])
            self.d3_u=self.D3.filter_march(self.setpoint['gamma']-self.cstate['gamma'])
	    dL = (self.d1_u-self.d3_u)*255
	    dR = (self.d1_u+self.d3_u)*255
	    self.motor_left.set_pwm(dL)
            self.motor_right.set_pwm(dR)

	    print(theta, self.encoder_left.speed,  self.encoder_right.speed, dL, dR)

	    time.sleep(DT)

    def pause(self):
        self.motor_left.stop()
        self.motor_right.stop()

        self.encoder_left.reset()
        self.encoder_right.reset()


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
