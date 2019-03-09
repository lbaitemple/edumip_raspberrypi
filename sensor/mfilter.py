import datetime
import math
from collections import deque

zero_tolerance=1e-8

class ModifiedFilter:

    def __init__(self, dt=0, num=[], den=[]):
        self.dt = dt
        self.num = num
        self.den = den
        self.order = len(den)-1
        self.initialized =1
        self.in_buf=deque(maxlen=len(den))
        self.out_buf=deque(maxlen=len(den))
        self.newest_input= 0.0
	self.newest_output = 0.0
	self.sat_flag = 0
        self.ss_en = 0
 	self.ss_step = 0
        self.sat_en =0
        self.sat_min =0
        self.sat_max =0
	self.step =0

    def filter_pid(self, kp, ki, kd, Tf, dt):
	self.step =0
        self.initialized =1
        self.newest_input= 0.0
        self.newest_output = 0.0
        self.sat_flag = 0
        self.ss_en = 0
        self.ss_step = 0
        self.sat_en =0
        self.sat_min =0
        self.sat_max =0

	if(Tf <= dt/2):
	    return -1
	if((math.fabs(ki)<zero_tolerance) and (math.fabs(kd)>zero_tolerance)):
	    self.num =[(kp*Tf+kd)/Tf, ((kp*(dt-Tf))-kd)/Tf]
	    self.den =[1.0 -(Tf-dt)/Tf]
	    self.order =1
	elif((math.fabs(ki)>zero_tolerance) and (math.fabs(kd)<zero_tolerance)):
	    self.num=[ kp, ((ki*dt)-kp)]
	    self.den = [1.0, -1.0]
            self.order =1
	# 0th order proportional gain only
	elif((math.fabs(ki)<zero_tolerance) and (math.fabs(kd)<zero_tolerance)):
            self.num=kp
            self.den = 1.0
            self.order =0
	#otherwise 2nd order PID with roll off
	else:
            self.num=[(kp*Tf+kd)/Tf, (ki*dt*Tf + kp*(dt-Tf) - kp*Tf - 2.0*kd)/Tf, (((ki*dt-kp)*(dt-Tf))+kd)/Tf]
            self.den = [1.0, (dt-(2.0*Tf))/Tf, (Tf-dt)/Tf]
            self.order =2

        self.in_buf=deque(maxlen=self.order)
        self.out_buf=deque(maxlen=self.order)
	self.gain =1

    def filter_enable_soft_start(self, seconds):
	self.ss_en	= 1;
	self.ss_steps	= seconds/self.dt;

    def filter_enable_saturation(self, min, max):
        self.sat_en =1
        self.sat_min =min
        self.sat_max =max


    def filter_print(self):
	print("order: ", self.order);
	print("timestep dt: ", self.dt);

	# print numerator
	print(self.num);
	print("--------");
        print(self.den)


    def filter_march(self, new_input):
	tmp1=0.0
        tmp2=0.0
	self.newest_input = new_input
        self.in_buf.append(new_input)
        num_len = min(len(self.in_buf), len(self.num))
        den_len = min(len(self.out_buf), len(self.den))

	for i in range(0, num_len):
#	    print("in", i, self.in_buf[-(i+1)], self.num[i])
	    tmp1 += self.in_buf[-(i+1)]*self.num[i]

	tmp1 = tmp1*self.gain
        for i in range(0, den_len-1):
#            print("out", i, self.out_buf[-(i+1)], self.den[i+1])
            tmp2 -= self.out_buf[-(i+1)]*self.den[i+1]

	new_out=tmp2+tmp1;
	new_out = new_out/self.den[0];

	if (self.ss_en and self.step<self.ss_steps):
	    a=self.sat_max*(self.step/self.ss_steps);
	    b=self.sat_min*(self.step/self.ss_steps);
	    if(new_out>a):
	        new_out=a;
	    if(new_out<b): 
	        new_out=b;

	# saturate and set flag
	if (self.sat_en):
	    if(new_out>self.sat_max):
	        new_out=self.sat_max
		self.sat_flag=1
	    elif(new_out<self.sat_min):
		new_out=self.sat_min;
		self.sat_flag=1;
	    else:
 		self.sat_flag=0;
	# record the output to filter struct and ring buffer
	self.newest_output = new_out
	self.out_buf.append(new_out)
	# increment steps
	self.step =self.step + 1 
	return new_out
