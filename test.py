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
#hashing
import hashlib
haslib.sha256(messageinbytes).hexdigest()


#print(d.decode('UTF-8'))
#end

'''
Python 3.10.5 (main, Jun  8 2022, 09:26:22) [GCC 11.3.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> ma = {'ad':3,'4':14}
>>> type(ma)
<class 'dict'>
>>> str(ma)
"{'ad': 3, '4': 14}"
>>> dict(str(ma))
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ValueError: dictionary update sequence element #0 has length 1; 2 is required
>>> import ast
>>> ast.literal_eval(str(ma))
{'ad': 3, '4': 14}
>>> x=ast.literal_eval(str(ma))
>>> type(x)
<class 'dict'>
>>> 
'''
