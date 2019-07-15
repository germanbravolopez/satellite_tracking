from pexpect import pxssh
import getpass

try:
	s1 = pxssh.pxssh()
	hostname = "172.16.3.10"
	username = "pi"
	password = "raspberry" #getpass.getpass('password: ')
	s1.login (hostname, username, password)
	s1.sendline ('sudo killall python')
	s1.logout()
except pxssh.ExceptionPxssh, e:
        print "pxssh failed on login."
	print str(e)
