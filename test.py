from socket import *

'''
s=socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.sendto('this is testing'.encode(),('255.255.255.255',12345))
'''
import rsa

pub,pri = rsa.newkeys(512)
print(type(pub))
s = pub.save_pkcs1()
print(type(s))
e= s.decode('UTF-8')
print(type(e))

print(e)

d = rsa.PublicKey.load_pkcs1(e.encode('UTF-8'))
print(type(d))
print(d)
d=d.save_pkcs1()
print(d.decode('UTF-8'))
#print(d.decode('UTF-8'))
#end
