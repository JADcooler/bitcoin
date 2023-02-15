from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)

def send(string):
	s.sendto(string.encode(),('255.255.255.255',12345))

while(1):
	send(input('ENTER PANRA '))

