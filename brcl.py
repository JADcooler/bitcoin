from socket import *


s=socket(AF_INET, SOCK_DGRAM)
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
s.sendto('this is testing'.encode(),('255.255.255.255',12345))



s=socket(AF_INET, SOCK_DGRAM)
s.bind(('',12345))
m=s.recvfrom(1024)
print(m[0])


'''
Pubkey hashes are almost always sent encoded as Bitcoin addresses,
 which are base58-encoded strings containing an address version number, the hash, and an error-detection checksum to catch typos. 


wallet options are

1. show public key hash 
2. show balance

'''
  
