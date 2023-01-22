from ecdsa import SigningKey
from ecdsa import BadSignatureError


sk = SigningKey.generate()
vk = sk.verifying_key
with open("ecc_private.pem", "wb") as f:
    f.write(sk.to_pem())
with open("ecc_public.pem", "wb") as f:
    f.write(vk.to_pem())
print(str(sk.verifying_key) )
print(str(sk.verifying_key) )

import hashlib

s=hashlib.sha256(b's').hexdigest()+str('1')
print(s)
x=sk.sign(s.encode())

message = s

print(type(x),x)


with open('test.txt',mode='wb') as file:
	file.write(x)

with open('test.txt',mode='rb') as file:
	x=file.read()
print(type(x),x)

try:
	vk.verify(x, message.encode())
	print("GOOD SIGNATURE")
except BadSignatureError:
	print("BAD SIGNATURE")

#end



