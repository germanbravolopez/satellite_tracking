"""
Server for one base station
"""

import sys
import socket
import select
import pickle


host = ''
portRaspi = 50002
backlog = 5
size = 1024

socketServos = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socketServos.bind((host,portRaspi))
socketServos.listen(backlog)

input_socket = [socketServos, sys.stdin]

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
f.write('600')
f.close()

#print ("Hello from server raspi 14")
print ("Hello from server raspi 10")
running = 1

positionServer = "900"

while running:

	f = open ('/sys/class/lse-pwm18/pwm/duty18','w')
	f.write(positionServer)
	f.close()

	inputready, outputready, exceptready = select.select(input_socket,[],[])
	for s in inputready:

		if s == socketServos:
			# handle Raspberry server socket
			clientRaspi, address = s.accept()
			msg = clientRaspi.recv(size)
			msg = pickle.loads(msg)
			clientRaspi.close()

			positionClient = msg[0]

			if (positionClient != positionServer):
				positionServer = str(positionClient)
			f = open('/sys/class/lse-pwm19/pwm/duty19','w')
			f.write('600')
			f.close()

		"""
		elif s == sys.stdin:
			# handle std inputs
			junk = sys.stdin.readline()

			if junk == "end\n":
				print("Closed Server")
				s.close()
				running = 0

			elif (500 < int(junk) < 999):
				positionServer = junk

		else:
			# handle all other sockets
			data = s.recv(size)
			if data:
				s.send(data)
			else:
				s.close()
				input_socket.remove(s)
		"""
socketServos.close()

