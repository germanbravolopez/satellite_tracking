from pexpect import pxssh
import getpass

import sys, time, os

print("Installing drivers BS 6...")

# Drivers
os.system("sudo rmmod lse_pwm18")
os.system("sudo rmmod lse_pwm19")

#os.system("clear")

os.system("sudo insmod /home/pi/satellite/lse_pwm18.ko")
os.system("sudo insmod /home/pi/satellite/lse_pwm19.ko")

print("")

# SSH
try:
    s = pxssh.pxssh()
    hostname = "172.16.3.10"
    username = "pi"
    password = "raspberry" #getpass.getpass('password: ')
    s.login (hostname, username, password)
    print('SSH connection successful')

    print("")
    print("Installing drivers in BS...")
    print("")

    s.sendline ('sudo rmmod lse_pwm18 &')   # run a command
    s.prompt()             # match the prompt
    print (s.before)          # print everything before the prompt.

    s.sendline ('sudo rmmod lse_pwm19 &')
    s.prompt()
    print (s.before)

    s.sendline ('sudo insmod /home/pi/satellite/lse_pwm18.ko &')
    s.prompt()
    print (s.before)

    s.sendline ('sudo insmod /home/pi/satellite/lse_pwm19.ko &')
    s.prompt()
    print (s.before)

    print("")
    print("Launching data receiver in BS 10...")
    print("")

    s.sendline ('python /home/pi/satellite/uart.py &')
    s.prompt()
    print s.before

    s.sendline ('sudo python /home/pi/satellite/raspi10/server_10.py &')
    s.prompt()
    print (s.before)

    s.sendline ('sudo python /home/pi/satellite/raspi10/client_10.py &')
    s.prompt()
    print s.before

    s.logout()

except pxssh.ExceptionPxssh, e:
    print ("pxssh failed on login.")
    print (str(e))


# Client
os.system("python /home/pi/satellite/uart.py &")
os.system("sudo python /home/pi/satellite/raspi6/client_6.py &")

time.sleep(6)

print("")
print("Ready for tracking...")
print("")

while True:
        matar=(raw_input("Print yes for closing: "))
        #print(matar)
        if (matar == "yes"):
                try:
		   s1 = pxssh.pxssh()
   		   hostname = "172.16.3.10"
    		   username = "pi"
    		   password = "raspberry" #getpass.getpass('password: ')
    		   s1.login (hostname, username, password)
		   s1.sendline ('sudo killall python')
		   s1.logout()
		except pxssh.ExceptionPxssh, e:
		   print ("pxssh failed on login.")
    		   print (str(e))

		os.system("sudo killall python")

		break

