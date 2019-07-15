"""
Client for the communication with the other base station
"""


import sys
import socket
import select
import pickle
import subprocess
from time import sleep
from foto import tracking_completo

host = '172.16.3.10'
port = 50002
size = 1024
socketServos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Activate PWM
f = open ('/sys/class/lse-pwm18/pwm/active18','w')
f.write('1')
f.close()

f = open ('/sys/class/lse-pwm19/pwm/active19','w')
f.write('1')
f.close()

# Set freq 50 Hz
f = open ('/sys/class/lse-pwm18/pwm/frequency18','w')
f.write('50')
f.close()

f = open ('/sys/class/lse-pwm19/pwm/frequency19','w')
f.write('50')
f.close()

# Initializate
f = open ('/sys/class/lse-pwm19/pwm/duty19','w') # servo horizontal
f.write('560')
f.close()

f = open ('/sys/class/lse-pwm18/pwm/duty18','w') # servo vertical
f.write('990')
f.close()

ack = 0
po = 0

socketServos.connect((host,port))
running = 1

while running:

	f = open ('/sys/class/lse-pwm18/pwm/duty18','r')
	pos_servo_vert = f.read()
	pos_servo_vert = pos_servo_vert[0:3]
	f.close()

	f = open ('/sys/class/lse-pwm19/pwm/duty19','r')
	pos_servo_hor = f.read()
	pos_servo_hor = pos_servo_hor[0:3]
	f.close()

#	print ('Pos_vert: '+str(pos_servo_vert)+'Pos_horiz: '+str(pos_servo_hor))

	pos_pelota = tracking_completo()

	if (ack == 0):
#		print('Servo raspi6 ready to move')
		ack = 1

	if((pos_pelota == 1) or (pos_pelota == 2) or (pos_pelota == 3)):
		po = int(pos_servo_vert) - 10
		if(450 <= po <= 989):
			f = open('/sys/class/lse-pwm18/pwm/duty18','w')
			f.write(str(po))
			f.close()

	if((pos_pelota == 7) or (pos_pelota == 8) or (pos_pelota == 9)):
		po = int(pos_servo_vert) + 10
		if(450<= po <= 989):
			f = open('/sys/class/lse-pwm18/pwm/duty18','w')
			f.write(str(po))
			f.close()

	if((pos_pelota == 1) or (pos_pelota == 4) or (pos_pelota == 7)):
		if(int(pos_servo_vert) > 650):
			po = int(pos_servo_hor) + 10
		else:
			po = int(pos_servo_hor) - 10
		if(250 <= po <= 989):
			f = open('/sys/class/lse-pwm19/pwm/duty19','w')
			f.write(str(po))
			f.close()

	if((pos_pelota == 3) or (pos_pelota == 6) or (pos_pelota == 9)):
		if (int(pos_servo_vert) > 650):
			po = int(pos_servo_hor) - 10
		else:
			po = int(pos_servo_hor) + 10

		if(250<= po <= 989):
			f = open('/sys/class/lse-pwm19/pwm/duty19','w')
			f.write(str(po))
			f.close()

	if (int(pos_servo_vert) == 450):
		pos_a_mandar = 550
		msg = pickle.dumps([pos_a_mandar])
		socketServos.send(msg)
		socketServos.close()
		socketServos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		socketServos.connect((host,port))

		#pos_tmp_v = int(pos_servo_vert)
		#pos_tmp_h = int(pos_servo_hor)

		f = open('/sys/class/lse-pwm18/pwm/duty18', 'w')
		f.write(str(990))
		f.close()

		f = open('/sys/class/lse-pwm19/pwm/duty19', 'w')
		f.write(str(560))
		f.close()
