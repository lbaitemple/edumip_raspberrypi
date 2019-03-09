DEBUG = True
wiringport = {
                2: 8,
                3: 9,
		4 : 7,
		17 : 0,
                27: 2,
		22 : 3,
		10 : 12,
		9 : 13,
		11 : 14,
                0: 30,
                5: 21, 
                6: 22,
                13: 23,
                14 : 15,
                15: 16,
                19: 24,
                26: 25,
                16: 27,
                19: 24,
                15 : 16,
                18 : 1,
                23 : 4,
                24 : 5,
                25 : 6, 
                8 : 10,
                7 : 11,
                1: 31,
               12: 26,
               16: 27,
               20: 28,
               21: 29,
                27 : 2
	}


PINS = {
    'motor': {
        'left': [24, 25],
        'right': [19, 16]
    },
    'encoder': {
        'left': [22, 23],
        'right': [15, 14]
    }
}

pid_params = {
    'balance': {
        'k': 0.6,
        'p': 20,
        'd': 0.06
    },
    'velocity': {
        'p': 8,
        'i': 0.001
    },
    'turn': {
        'p': 0.4,
        'd': 0.2
    }
}

gyro_offset = {
    'y': 1.4,
    'z': 0.7
}
accel_offset = {
    'x': -230,
    'y': -1.5,
    'z': -14100
}

SAMPLE_RATE_HZ=100
DT=0.01

# Structural properties of eduMiP
BOARD_MOUNT_ANGLE =0.49 # increase if mip tends to roll forward
GEARBOX	= 35.577
ENCODER_RES = 60
WHEEL_RADIUS_M	= 0.034
TRACK_WIDTH_M	= 0.035
V_NOMINAL =7.4
THETA_REF_MAX=0.33

DRIVE_RATE_ADVANCED=16
TURN_RATE_ADVANCED=6

TIP_ANGLE=0.85
START_ANGLE=0.3
START_DELAY=0.4
PICKUP_DETECTION_TIME=0.6
ENABLE_POSITION_HOLD=1
STEERING_INPUT_MAX=0.5
edumip_params ={
  'BOARD_MOUNT_ANGLE': 0.49,
  'GEARBOX': 35.577,
  'ENCODER_RES': 60,
  'WHEEL_RADIUS_M': 0.034,
  'TRACK_WIDTH_M': 0.035,
  'V_NOMINAL': 7.4,
  'D1': {
      'gain': 1.05,
      'order': 2,
      'num': [-4.945, 8.862, -3.967],
      'den': [ 1.000, -1.481, 0.4812],
      'saturation_timeout': 0.4
  },
  'D2': {
      'gain': 0.9,
      'order': 2,
      'num': [0.18856,  -0.37209,  0.18354],
      'den': [1.00000,  -1.86046,   0.86046],
      'theta_ref_max': 0.33
   },
  'D3': {
     'kp': 1.0,
     'ki': 0.3,
     'kd': 0.05,
     'steering_max': 0.5
   }
}
